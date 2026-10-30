#!/usr/bin/env python3
"""Small deterministic routing SMOKE TEST for Cinematic DNA.

The skill's model must use semantic understanding too; a keyword router cannot
replace intent recognition. This script never accesses YouTube or generates media.
"""
import re
import sys
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s<>\]\[()]+", re.I)
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be", "www.youtu.be", "music.youtube.com"}


def youtube_urls(message):
    found = []
    for candidate in URL_RE.findall(message):
        candidate = candidate.rstrip(".,!?;:)")
        try:
            parsed = urlparse(candidate)
        except ValueError:
            continue
        if (parsed.hostname or "").lower() in YOUTUBE_HOSTS and candidate not in found:
            found.append(candidate)
    return found


def classify(message):
    s = message.casefold().strip()
    urls = youtube_urls(message)
    # Priority: explicit user intent always beats the bare-link default.
    if re.fullmatch(r"(?:дальше|продолжай|продолжить|continue|next)[\s.!?]*", s):
        return "CONTINUE"
    if re.search(r"исправ|передел|почин|fix|repair|дерга|зум", s):
        return "REPAIR"
    if re.search(r"сравн|compare|отличи", s):
        return "COMPARE"
    if re.search(r"сколько\s+стоит|стоимост|цены|бюджет|budget|cost|pricing", s):
        return "BUDGET"
    if re.search(r"название|описани|обложк|thumbnail|packaging|title", s):
        return "PACKAGE"
    if re.search(r"только\s+анализ|разбери|анализир|анализ|analy[sz]e", s):
        return "ANALYZE"
    if re.search(r"иде[июйи]|сценар|story\s+ideas|pitch", s) and not re.search(r"сделай\s+(?:видео|ролик|фильм)|создай\s+(?:видео|ролик|фильм)", s):
        return "IDEATE"
    if len(urls) > 1:
        return "MULTI_REF"
    if re.search(r"сделай|создай|сними|хочу\s+(?:такой|похож|свой)|produce|create|film", s):
        return "CREATE"
    if len(urls) == 1:
        return "ONE_LINK_STUDIO"
    return "UNSPECIFIED"


if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    print(classify(message))
