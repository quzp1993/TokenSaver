import re
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
text = open("answers.md", encoding="utf-8").read()

# Split into question blocks: "# Q<n>"
blocks = re.split(r"^# Q(\d+)\s*$", text, flags=re.M)
rows = []
totals = {"S1": 0, "S2": 0, "S3": 0}
for i in range(1, len(blocks), 2):
    qnum = blocks[i]
    content = blocks[i + 1]
    for m in re.finditer(r"^## S(\d+)\s*\n(.*?)(?=^## S|\Z)", content, flags=re.M | re.S):
        s = f"S{m.group(1)}"
        body = m.group(2).strip()
        n = len(enc.encode(body))
        rows.append((int(qnum), s, n))
        totals[s] += n

print(f"{'Q':>3} {'S1':>5} {'S2':>5} {'S3':>5}  {'S1-S3 save':>10}")
by_q = {}
for q, s, n in rows:
    by_q.setdefault(q, {})[s] = n
for q in sorted(by_q):
    a = by_q[q].get("S1", 0)
    b = by_q[q].get("S2", 0)
    c = by_q[q].get("S3", 0)
    save = f"{100*(a-c)/a:6.1f}%" if a else "  n/a"
    print(f"{q:>3} {a:>5} {b:>5} {c:>5}  {save:>10}")

t1, t2, t3 = totals["S1"], totals["S2"], totals["S3"]
print("-" * 42)
print(f"{'Σ':>3} {t1:>5} {t2:>5} {t3:>5}  {100*(t1-t3)/t1:6.1f}%")
print(f"\nS2 vs S1: -{100*(t1-t2)/t1:.1f}%   S3 vs S1: -{100*(t1-t3)/t1:.1f}%   S3 vs S2: -{100*(t2-t3)/t2:.1f}%")
