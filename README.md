# TokenSaver

Token-saving pipeline for Claude Code. One install wires three compression levers. Like prokka wiring prodigal/hmmer/aragorn into one annotation pipeline, TokenSaver orchestrates rtk plus its own rules instead of reimplementing them.

## What it is

TokenSaver is an orchestrator, not another compressor. Each lever is handled by the best tool:

| Lever | Engine | What it does |
|---|---|---|
| Input | **rtk** (integrated) | compress / aggregate / truncate command output before it reaches the model |
| Output | TokenSaver skill | minimum-token answers, every technical fact kept |
| Context | TokenSaver hooks | lean CLAUDE.md pointers + on-demand files, rules auto-injected |

## Features

- `SessionStart` / `SubagentStart` hook injects the ruleset every session — savings are automatic, no manual invocation.
- `PreToolUse` hook compacts `git status` → `--short`, `git log` → `--oneline -n 30` (lossless whitelist).
- `setup.sh` — one command wires rtk (installs + global hook) and installs the plugin.
- Skill rules cover output (zero-prose code), input (rtk / compact flags / pipe), context (one-line pointers).

## Strategy

1. **Do not reimplement specialized tools.** Input compression is rtk's job; TokenSaver calls rtk, adds its own lossless git rewrites, and owns the output + context levers.
2. **Output wins by dropping prose, never facts.** Code/SQL/shell with zero prose, facts as comma lists or `key: value`, no decorative glyphs, negations always kept.
3. **Context trades a fixed 193-token ruleset injection for always-on enforcement** across all three levers.

## Install

```bash
bash setup.sh
```

Manual: `claude plugin marketplace add quzp1993/TokenSaver && claude plugin install token-saver@token-saver` (rtk via winget / brew).

## Combined benchmark

Reference session = 10 Q&A + 4 command types + 1 session start:

| Lever | baseline | TokenSaver | saved |
|---|---|---|---|
| output | 1644 | 479 | −70.9% |
| input | 144256 | 414 | −99.7% |
| context | 707 | 296 | −58.1% |
| **total** | **146607** | **1189** | **−99.2%** |

Context savings scale with how bloated the original CLAUDE.md is (real projects 1000–8000 tokens save proportionally more). Full tables and scripts in [`benchmark/`](benchmark/).

## Structure

```
.claude-plugin/   manifest + marketplace
skills/           the skill
src/hooks/        session-start.js, pre-tool-use.js
setup.sh          one-command installer (wires rtk)
benchmark/        questions, answers, count.py, input_bench.py, combined_bench.py, results.md
```

## License

MIT
