"""Ask real LLMs through APIpod (streaming /v1/chat/completions; non-stream calls time out at 524).
Usage: python3 ask.py <log.json> <model> "<question>"  - appends the turn to the model's thread in the log, prints the answer.
Key: /home/claude/.apipod_key (never printed). The full log is the evidence for the video."""
import json, os, sys, time, urllib.request
KEY = open("/home/claude/.apipod_key").read().strip()


def chat(model, messages, timeout=240):
    body = json.dumps({"model": model, "stream": True, "messages": messages}).encode()
    r = urllib.request.Request("https://api.apipod.ai/v1/chat/completions", data=body, method="POST",
                               headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json", "User-Agent": "curl/8.5.0"})
    out, t0 = [], time.time()
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        for line in resp:
            line = line.decode().strip()
            if not line.startswith("data:") or line == "data: [DONE]":
                if line == "data: [DONE]":
                    break
                continue
            ch = json.loads(line[5:])["choices"]
            if not ch:
                continue
            out.append(ch[0].get("delta", {}).get("content") or "")
            if ch[0].get("finish_reason") in ("stop", "length"):
                break                                  # APIpod tags normal Gemini chunks "content_filter": do not stop on it
    return "".join(out).strip()


if __name__ == "__main__":
    log, model, q = sys.argv[1], sys.argv[2], sys.argv[3]
    d = json.load(open(log)) if os.path.exists(log) else {}
    th = d.setdefault(model, [])
    msgs = [{"role": t["role"], "content": t["content"]} for t in th] + [{"role": "user", "content": q}]
    a = chat(model, msgs)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    th += [{"role": "user", "content": q, "ts": ts}, {"role": "assistant", "content": a, "ts": ts}]
    json.dump(d, open(log, "w"), indent=1, ensure_ascii=False)
    print(f"[{model}] {a}")
