"""Delivered resolution vs ordered resolution (owner 07.11: 'Проверяй разрешение сразу, нужно чтоб мы получали разрешение какое заказывали').
Usage: python3 tools/check_resolution.py <file> <ordered_height_p e.g. 720> [aspect w:h, default 9:16]
Ordered 720p 9:16 = 720x1280 (4K still 9:16 = 2160x3840). Exact = PASS; width/height off by at most 1 % = NOTE (model rounding, reported); more = FAIL.
Also importable: check(path, p, aspect) -> (status, text). Generation scripts call it right after the download and print the result."""
import json, subprocess, sys

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", path],
                         capture_output=True, text=True).stdout
    s = json.loads(out)["streams"][0]
    return int(s["width"]), int(s["height"])

def expected(p, aspect="9:16"):
    aw, ah = (int(x) for x in aspect.split(":"))
    # the short side is the ordered "p" for vertical and horizontal alike
    if aw <= ah:
        return p, round(p * ah / aw)
    return round(p * aw / ah), p

def check(path, p, aspect="9:16"):
    w, h = probe(path)
    ew, eh = expected(p, aspect)
    if (w, h) == (ew, eh):
        return "PASS", "resolution %dx%d = ordered %dx%d" % (w, h, ew, eh)
    dev = max(abs(w - ew) / ew, abs(h - eh) / eh)
    status = "NOTE" if dev <= 0.01 else "FAIL"
    return status, "resolution %dx%d, ordered %dx%d (%s, off by %.2f %%)" % (w, h, ew, eh, status, dev * 100)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    st, txt = check(sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "9:16")
    print(st, txt)
    sys.exit(1 if st == "FAIL" else 0)
