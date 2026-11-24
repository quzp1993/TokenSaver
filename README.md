# TokenSaver

Claude Code plugin that saves tokens on three levers: **output** (reply), **input** (command output), **context** (persistent files).

## Install

```bash
claude plugin marketplace add quzp1993/TokenSaver
claude plugin install token-saver@token-saver
```

Skill only, no hooks:

```bash
npx skills add quzp1993/TokenSaver
```

## Three levers

- **Output** — minimum-token answers: code/SQL/shell with zero prose, facts as comma lists or `key: value`, no decorative glyphs, negations never dropped.
- **Input** — command-output hygiene: batch commands, compact flags, pipe noisy output down, grep instead of cat, read only log tails. A `PreToolUse` hook compacts `git status` → `git status --short` and `git log` → `git log --oneline -n 30` automatically.
- **Context** — lean persistent files: one-line pointers in CLAUDE.md, offload reference to files read on demand. A `SessionStart` hook injects the full ruleset every session so the rules stay active without manual invocation.

## Benchmark (three levers)

**Output** — 10 questions, 3 strategies, cl100k_base:

| Strategy | tokens | vs baseline | key-info retention |
|---|---|---|---|
| baseline | 1644 | — | 100% |
| caveman | 577 | −64.9% | 100% |
| **TokenSaver** | **479** | **−70.9%** | **100%** |
| hybrid (best per question) | 459 | −72.1% | 100% |

**Input** — real command output, raw vs token-saver hook vs rtk:

| command | raw | token-saver | rtk |
|---|---|---|---|
| git status | 23 | 0 | 12 |
| git log | 438 | 49 | 203 |
| ls -la ~/.claude | 776 | — | 185 |
| find ~/.claude/plugins -type f | 143019 | — | 14 |
| **total** | **144256** | **143844** | **414** (−99.7%) |

**Context** — global CLAUDE.md + RTK.md load at **103 tokens** (pointer pattern); token-saver ruleset injection costs 193 tokens/session to keep all three levers automatic.

Reproducible data and scripts: [`benchmark/`](benchmark/).

## Structure

```
.claude-plugin/plugin.json      manifest + hooks
.claude-plugin/marketplace.json marketplace entry
skills/token-saver/SKILL.md     the skill
src/hooks/session-start.js      injects ruleset every session
src/hooks/pre-tool-use.js       compacts git status / git log
```

## License

MIT
