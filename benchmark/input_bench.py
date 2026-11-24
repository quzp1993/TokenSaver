import subprocess
import shutil
import os
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")


def T(s):
    return len(enc.encode(s))


rtk = shutil.which("rtk") or r"C:\Program Files\WinGet\Links\rtk.exe"


def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return (r.stdout or "") + (r.stderr or "")


TS_REPO = r"e:\1_workfile\4_其他\1_微新生物\_ts4"
HOME = os.path.expanduser("~")

# (label, raw command, token-saver command or None, cwd)
cases = [
    ("git status", "git status", "git status --short", TS_REPO),
    ("git log", "git log", "git log --oneline -n 30", TS_REPO),
    ("ls -la ~/.claude", "ls -la ~/.claude", None, None),
    ("find ~/.claude/plugins -type f", "find ~/.claude/plugins -type f", None, None),
]

print(f"{'command':<28} {'raw':>6} {'toksaver':>9} {'rtk':>6} {'toksaver%':>9} {'rtk%':>8}")
tot_raw = tot_ts = tot_rtk = 0
for label, rawc, tsc, cwd in cases:
    raw = run(f'"{rtk}" bypass {rawc}', cwd)
    ts = run(f'"{rtk}" bypass {tsc}', cwd) if tsc else None
    rk = run(f'"{rtk}" {rawc}', cwd)
    rt, kt = T(raw), T(rk)
    st = T(ts) if ts is not None else rt
    tot_raw += rt
    tot_ts += st
    tot_rtk += kt

    def pct(a, b):
        return f"{100*(a-b)/a:.0f}%" if a else "-"

    ts_s = str(st) if ts is not None else "-"
    print(f"{label:<28} {rt:>6} {ts_s:>9} {kt:>6} {pct(rt, st):>9} {pct(rt, kt):>8}")

print(f"{'TOTAL':<28} {tot_raw:>6} {tot_ts:>9} {tot_rtk:>6} {pct(tot_raw, tot_ts):>9} {pct(tot_raw, tot_rtk):>8}")
