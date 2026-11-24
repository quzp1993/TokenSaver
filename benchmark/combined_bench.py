import subprocess
import shutil
import os
import re
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")


def T(s):
    return len(enc.encode(s))


def pct(a, b):
    return f"{100*(a-b)/a:.1f}%" if a else "-"


# ---- OUTPUT lever: re-count answers.md (S1 baseline, S3 token-saver) ----
txt = open("answers.md", encoding="utf-8").read()

out_base = out_ts = 0
for blk in re.split(r"^# Q\d+\s*$", txt, flags=re.M)[1:]:
    for m in re.finditer(r"^## S(\d+)\s*\n(.*?)(?=^## S|\Z)", blk, flags=re.M | re.S):
        n = T(m.group(2).strip())
        if m.group(1) == "1":
            out_base += n
        elif m.group(1) == "3":
            out_ts += n

# ---- INPUT lever: real command output, raw vs rtk ----
rtk = shutil.which("rtk") or r"C:\Program Files\WinGet\Links\rtk.exe"


def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return (r.stdout or "") + (r.stderr or "")


TS_REPO = r"e:\1_workfile\4_其他\1_微新生物\_ts4"
HOME = os.path.expanduser("~")
cases = [
    ("git status", TS_REPO),
    ("git log", TS_REPO),
    ("ls -la ~/.claude", None),
    ("find ~/.claude/plugins -type f", None),
]
in_raw = in_rtk = 0
for c, cwd in cases:
    in_raw += T(run(f'"{rtk}" bypass {c}', cwd))
    in_rtk += T(run(f'"{rtk}" {c}', cwd))

# ---- CONTEXT lever ----
def ft(p):
    return T(open(p, encoding="utf-8").read())


lean_cm = ft(os.path.join(HOME, ".claude", "CLAUDE.md"))
rtk_md = ft(os.path.join(HOME, ".claude", "RTK.md"))
bloated = ft("bloated_claude.md")
ruleset = 193  # measured: token-saver SessionStart injection

ctx_base = bloated + rtk_md
ctx_opt = lean_cm + rtk_md + ruleset

base = out_base + in_raw + ctx_base
opt = out_ts + in_rtk + ctx_opt

print("=" * 64)
print("Reference session = 10 Q&A + 4 command types + 1 session start")
print("=" * 64)
print(f"{'lever':<10} {'baseline':>10} {'TokenSaver':>11} {'saved':>9}")
print(f"{'output':<10} {out_base:>10} {out_ts:>11} {pct(out_base, out_ts):>9}")
print(f"{'input':<10} {in_raw:>10} {in_rtk:>11} {pct(in_raw, in_rtk):>9}")
print(f"{'context':<10} {ctx_base:>10} {ctx_opt:>11} {pct(ctx_base, ctx_opt):>9}")
print("-" * 64)
print(f"{'TOTAL':<10} {base:>10} {opt:>11} {pct(base, opt):>9}")
