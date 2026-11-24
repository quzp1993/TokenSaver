# TokenSaver

Claude Code skill that saves tokens on three levers: **output** (reply), **input** (command output), **context** (persistent files).

## Install

```bash
npx skills add quzp1993/TokenSaver
```

or copy `SKILL.md` to `~/.claude/skills/token-saver/SKILL.md`.

## Three levers

- **Output** — minimum-token answers: code/SQL/shell with zero prose, facts as comma lists or `key: value`, no decorative glyphs, negations never dropped.
- **Input** — command-output hygiene: batch commands, compact flags, pipe noisy output down, grep instead of cat, read only log tails.
- **Context** — lean persistent files: one-line pointers in CLAUDE.md, offload reference to files read on demand.

## Benchmark (output lever)

10 questions, 3 output strategies, token count via cl100k_base:

| Strategy | tokens | vs baseline | key-info retention |
|---|---|---|---|
| baseline | 1644 | — | 100% |
| caveman | 577 | −64.9% | 100% |
| **TokenSaver** | **479** | **−70.9%** | **100%** |
| hybrid (best per question) | 459 | −72.1% | 100% |

Reproducible data and script: [`benchmark/`](benchmark/).

## License

MIT
