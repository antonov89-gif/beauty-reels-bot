import sys, concurrent.futures as cf
sys.path.insert(0, "/home/claude/v14")
import ws
NEG = "text, letters, words, writing, captions, subtitles, logo, watermark, readable map labels, numbers, signature, modern objects"
P = {
 "a1_cartographer": "Late 16th-century Flemish cartographer's workshop, an elderly scholar in a dark wool robe and cap seen from behind and in profile, his face not in focus, drawing coastlines on a large parchment world map with a quill, brass dividers and a globe on the oak table, warm candlelight and window light from the left, dust in the air, painterly documentary realism, film grain. Slow dolly-in over his shoulder toward the parchment. No text, no letters, no readable writing, no logos.",
 "a2_ship": "Late 16th-century carrack under full sail on a deep blue Atlantic swell at golden hour, close-up of a brass compass and a rolled parchment chart on the wooden deck in the foreground, sails and rigging behind, sea spray, warm low sun, cinematic documentary realism, film grain. Slow push-in from the compass to the bow. No text, no letters, no flags with symbols, no logos.",
 "b1_ice": "Aerial view over the Greenland ice sheet edge, white ice field breaking into a deep blue fjord with floating icebergs, low Arctic sun, long shadows, crisp air, documentary drone realism. Slow forward drone flight toward the ice edge. No text, no people, no logos.",
 "b2_outback": "Aerial view over the Australian outback, red desert sand with dry riverbeds and sparse spinifex, a long straight red dirt road to the horizon, midday heat haze, documentary drone realism. Slow forward drone flight along the road. No text, no people, no vehicles with logos.",
}
def go(k):
    r = ws.run("google/veo3.1-lite/text-to-video", {"prompt": P[k], "negative_prompt": NEG, "aspect_ratio": "9:16", "duration": 4, "resolution": "720p"}, out=f"{k}.mp4", timeout=900)
    return k, r.get("status"), r.get("error") or r.get("code")
print("balance before", ws.balance(), flush=True)
with cf.ThreadPoolExecutor(4) as ex:
    for res in ex.map(go, P): print(res, flush=True)
print("balance after", ws.balance(), flush=True)
