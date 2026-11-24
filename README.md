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

## Benchmark (output lever)

10 questions, 3 output strategies, token count via cl100k_base:

| Strategy | tokens | vs baseline | key-info retention |
|---|---|---|---|
| baseline | 1644 | — | 100% |
| caveman | 577 | −64.9% | 100% |
| **TokenSaver** | **479** | **−70.9%** | **100%** |
| hybrid (best per question) | 459 | −72.1% | 100% |

Reproducible data and script: [`benchmark/`](benchmark/).

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
