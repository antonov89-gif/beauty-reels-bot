"""Titles, descriptions, tags for the 7 border/capital Shorts + publish slots (MSK, 10-16 h window; 2 per day).
Used to build the Metricool posts (YouTube Short + TikTok). Run: python3 publication.py > publication.json"""
import json
from scripts import SHORTS

DISCLOSE = ("Satellite imagery: Esri World Imagery (Esri, Maxar, Earthstar Geographics, and the GIS User Community); "
            "country borders: Natural Earth. Maps and diagrams are drawn for this video; route lines and the Bir Tawil lines are simplified. "
            "Voice-over is AI (ElevenLabs via Lumean).")

META = {
    "pointroberts": dict(
        slot="2026-10-25T10:00:00", tags=["point roberts", "point roberts washington", "us canada border", "49th parallel", "strange borders", "us exclave", "weird borders", "geography", "maps", "facts"],
        hashtags="#geography #map #borders #usa #canada #facts #shorts"),
    "guiana": dict(
        slot="2026-10-25T14:00:00", tags=["french guiana", "france brazil border", "longest border", "oyapock bridge", "guiana space centre", "kourou", "strange borders", "geography", "maps", "facts"],
        hashtags="#geography #map #borders #france #brazil #facts #shorts"),
    "velez": dict(
        slot="2026-10-26T10:00:00", tags=["shortest border in the world", "penon de velez de la gomera", "spain morocco border", "shortest land border", "strange borders", "weirdest borders", "geography", "maps", "facts"],
        hashtags="#geography #map #borders #spain #morocco #facts #shorts"),
    "sa3": dict(
        slot="2026-10-26T14:00:00", tags=["south africa capitals", "why south africa has 3 capitals", "pretoria", "cape town", "bloemfontein", "lesotho", "capital cities", "geography", "maps", "facts"],
        hashtags="#geography #map #southafrica #capitals #facts #shorts"),
    "llivia": dict(
        slot="2026-10-27T10:00:00", tags=["llivia", "llivia spain france", "spanish enclave", "exclave", "treaty of the pyrenees", "cerdanya", "strange borders", "geography", "maps", "facts"],
        hashtags="#geography #map #borders #spain #france #facts #shorts"),
    "angle": dict(
        slot="2026-10-28T10:00:00", tags=["northwest angle", "northwest angle minnesota", "us canada border", "lake of the woods", "us exclave", "strange borders", "weird borders", "geography", "maps", "facts"],
        hashtags="#geography #map #borders #usa #canada #facts #shorts"),
    "birtawil": dict(
        slot="2026-10-27T14:00:00", tags=["bir tawil", "bir tawil terra nullius", "egypt sudan border", "halaib triangle", "unclaimed land", "strange borders", "weirdest borders", "geography", "maps", "facts"],
        hashtags="#geography #map #borders #egypt #sudan #facts #shorts"),
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
