# TokenSaver

Claude Code skill that saves tokens. Answers in the fewest tokens that keep every technical fact.

## Install

```bash
npx skills add quzp1993/TokenSaver
```

or copy `SKILL.md` to `~/.claude/skills/token-saver/SKILL.md`.

## Benchmark

10 questions, 3 output strategies, token count via cl100k_base:

| Strategy | tokens | vs baseline | key-info retention |
|---|---|---|---|
| baseline | 1644 | — | 100% |
| caveman | 577 | −64.9% | 100% |
| **TokenSaver** | **479** | **−70.9%** | **100%** |
| hybrid (best per question) | 459 | −72.1% | 100% |

Reproducible data and script: [`benchmark/`](benchmark/).

## What it saves

- Code / SQL / shell requests: output only, no prose.
- Facts: comma lists or `key: value` lines, no bullets, arrows, or emoji.
- Drops articles and connectors, never drops negations, numbers, paths, or errors.
- Full sentences kept for security warnings, irreversible actions, multi-step order, and ambiguous questions.

## License

MIT
