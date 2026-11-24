import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import tiktoken
from anthropic import Anthropic

enc = tiktoken.get_encoding("cl100k_base")

# ---- config from ~/.claude/settings.json ----
home = os.path.expanduser("~")
cfg = json.load(open(os.path.join(home, ".claude", "settings.json"), encoding="utf-8"))
env = cfg.get("env", {})
base_url = env.get("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic")
api_key = env.get("ANTHROPIC_AUTH_TOKEN", "")
model = env.get("ANTHROPIC_DEFAULT_OPUS_MODEL", cfg.get("model", "deepseek-v4-pro"))

client = Anthropic(base_url=base_url, api_key=api_key)

# ---- three output strategies ----
SYSTEMS = {
    "S1_baseline": "Answer in Simplified Chinese. You are a helpful assistant. Answer the user's question fully, clearly, and politely, in complete sentences with explanations and examples.",
    "S2_caveman": "Answer in Simplified Chinese. Answer tersely like a smart caveman: no greeting, no filler, no articles where meaning survives. Keep every technical fact, number, code, command, and error verbatim. Short sentences.",
    "S3_tokensaver": "Answer in Simplified Chinese. Answer in the fewest tokens that keep every fact. Code/SQL/shell: output only the code, no prose. Facts: comma list or key:value, no bullets, no arrows, no emoji. Drop articles and connectors, never drop negations. Answer first.",
}

questions = json.load(open("questions.json", encoding="utf-8"))


def ask(q, system):
    for attempt in range(2):
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=1024,
                system=system,
                messages=[{"role": "user", "content": q}],
            )
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            return text, resp.usage.output_tokens
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            return f"[ERROR {e}]", 0
    return "", 0


def retention(answer, keys):
    low = answer.lower()
    hit = sum(1 for k in keys if k.lower() in low)
    return hit / len(keys) if keys else 1.0


def run_one(idx_q):
    idx, q = idx_q
    row = {"idx": idx, "cat": q["cat"], "q": q["q"]}
    for strat, sys in SYSTEMS.items():
        text, total = ask(q["q"], sys)
        row[strat + "_tokens"] = len(enc.encode(text))
        row[strat + "_total_tokens"] = total
        row[strat + "_retention"] = retention(text, q["keys"])
    return row


rows = []
N = len(questions)
t0 = time.time()
with ThreadPoolExecutor(max_workers=12) as ex:
    futs = {ex.submit(run_one, (i, q)): i for i, q in enumerate(questions)}
    done = 0
    for f in as_completed(futs):
        rows.append(f.result())
        done += 1
        if done % 20 == 0:
            print(f"{done}/{N} done, {time.time()-t0:.0f}s", flush=True)

rows.sort(key=lambda r: r["idx"])
json.dump(rows, open("results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- summary ----
def mean(xs):
    return sum(xs) / len(xs) if xs else 0

for strat in ["S1_baseline", "S2_caveman", "S3_tokensaver"]:
    toks = [r[strat + "_tokens"] for r in rows]
    ret = [r[strat + "_retention"] for r in rows]
    print(f"{strat}: tokens total={sum(toks)} mean={mean(toks):.1f} median={sorted(toks)[len(toks)//2]} | retention mean={mean(ret):.3f}")

base = sum(r["S1_baseline_tokens"] for r in rows)
for strat in ["S2_caveman", "S3_tokensaver"]:
    t = sum(r[strat + "_tokens"] for r in rows)
    print(f"{strat} vs baseline: -{100*(base-t)/base:.1f}%")

print(f"\ntotal API time {time.time()-t0:.0f}s")
