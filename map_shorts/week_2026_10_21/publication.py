"""Titles, descriptions, tags for the 7 geography Shorts + their publish slots (MSK, 10-16 h window).
Used to build the Metricool posts (YouTube Short + TikTok). Run: python3 publication.py > publication.json"""
import json
from scripts import SHORTS

DISCLOSE = ("Satellite imagery: Esri World Imagery (Esri, Maxar, Earthstar Geographics, and the GIS User Community); "
            "country borders: Natural Earth. Maps and diagrams are drawn for this video. Voice-over is AI (ElevenLabs via Lumean).")

META = {
    "pheasant": dict(
        slot="2026-10-21T10:00:00", tags=["pheasant island", "isle of pheasants", "spain france border", "treaty of the pyrenees", "bidasoa", "strange borders", "condominium", "geography", "maps", "facts"],
        hashtags="#geography #maps #borders #spain #france #facts #shorts"),
    "baarle": dict(
        slot="2026-10-21T14:00:00", tags=["baarle hertog", "baarle nassau", "belgium netherlands border", "enclaves", "exclaves", "strange borders", "weirdest border", "geography", "maps", "facts"],
        hashtags="#geography #maps #borders #belgium #netherlands #facts #shorts"),
    "bolivia": dict(
        slot="2026-10-22T10:00:00", tags=["bolivia navy", "landlocked country", "war of the pacific", "lake titicaca", "day of the sea", "bolivia chile", "geography", "maps", "history", "facts"],
        hashtags="#geography #maps #bolivia #chile #history #facts #shorts"),
    "egypt": dict(
        slot="2026-10-22T14:00:00", tags=["egypt population", "nile river", "why egypt is crowded", "egypt desert", "nile delta", "new administrative capital", "geography", "maps", "facts"],
        hashtags="#geography #maps #egypt #nile #facts #shorts"),
    "chile": dict(
        slot="2026-10-23T10:00:00", tags=["why is chile so long", "chile shape", "longest country", "andes", "atacama desert", "war of the pacific", "geography", "maps", "facts"],
        hashtags="#geography #maps #chile #andes #facts #shorts"),
    "canberra": dict(
        slot="2026-10-23T14:00:00", tags=["why canberra is the capital", "australia capital", "sydney vs melbourne", "canberra history", "walter burley griffin", "geography", "maps", "history", "facts"],
        hashtags="#geography #maps #australia #canberra #history #facts #shorts"),
    "diomede": dict(
        slot="2026-10-24T10:00:00", tags=["diomede islands", "international date line", "big diomede", "little diomede", "bering strait", "tomorrow island", "yesterday island", "geography", "maps", "facts"],
        hashtags="#geography #maps #diomede #dateline #russia #usa #facts #shorts"),
}


def build():
    out = []
    for k, s in SHORTS.items():
        m = META[k]
        text = "\n".join(s["lines"][:2]) + "\n\n" + s["facts"] + "\n\n" + DISCLOSE + "\n\n" + m["hashtags"]
        out.append(dict(key=k, title=s["title"], description=text, tags=m["tags"], slot=m["slot"], file=f"{k}/{k}.mp4"))
    return out


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=1))
