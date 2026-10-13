import ws302, concurrent.futures as cf
J = {
 "thumb28_a": "Cinematic photorealistic aerial drone photo of a very narrow sea strait between two dry rocky desert coastlines, many large oil tankers and container ships queued and stuck in the narrow channel, dramatic orange sunset sky, deep blue water, slight haze. Wide 16:9 composition, ships and strait in the right two thirds, calm empty sea on the left third for text. No text, no letters, no logos, no flags.",
 "thumb28_b": "Cinematic photorealistic aerial drone photo of a long freight train with containers crossing a vast golden desert between rugged brown mountains toward a distant sea with a container port and ships on the horizon, warm low sun, strong depth. Wide 16:9 composition, train on the right, open empty sky on the left third for text. No text, no letters, no logos, no flags.",
}
def go(k):
    r = ws302.run("bytedance/seedream-v4.5", {"prompt": J[k], "size": "2560*1440"}, out=f"{k}.jpg")
    return k, r.get("status"), str(r.get("error"))[:200]
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(go, J): print(r, flush=True)
