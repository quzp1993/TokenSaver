---
name: token-saver
description: Save tokens on three levers — output (minimum-token answers), input (command-output hygiene), context (lean persistent files). Use for "be brief", "less tokens", "save tokens", "省token", "省 token", or by default for low-risk explanations, code, SQL, and shell-command requests.
---

# TokenSaver

One skill, three levers: compress the reply, the command output, and the persistent context. Payload (code, commands, numbers, paths, errors) stays verbatim everywhere.

## Output — minimum-token answers

1. Answer first. No greeting, no recap, no closer, no "let me", no "好的", no "下面".
2. Code / SQL / shell request: output only the code block, no surrounding prose. Add one short caveat only when safety or a negation depends on it.
3. Facts: comma-separated list, or `key: value` lines. No bullet glyphs (· - •), no arrows, no emoji, no decorative markers.
4. Drop articles and connectors where the sentence still reads in one pass. Never drop negations: not / never / no / only / except / 未 / 勿 / 不能.
5. One idea per line. Numbers and units exact.

## Input — command-output hygiene

6. Batch related commands into one call.
7. Prefer compact flags: `git status --short`, `git diff --stat`, `git log --oneline -n`.
8. Pipe noisy output down: `… | tail -n 20`, `… 2>&1 | tail`, drop known-noise lines with `grep -v`.
9. Do not `cat` large files. Read with `offset`/`limit`, or Grep a pattern.
10. Build or test logs go to a file, read only the tail.
11. Truncated output states its recovery path in its own text. Use that path instead of re-running the whole command.

## Context — lean persistent context

12. Keep CLAUDE.md and global instructions short: one-line pointer per topic.
13. Long reference content goes to files, read on demand, never pasted whole.
14. Memory index: one line per memory.
15. Cite file paths instead of re-pasting blocks already in context.

## Break to full sentences when

- Security warning, or an irreversible / destructive action.
- A multi-step order that a fragment could scramble.
- The user is confused or repeated the question.
- The text must survive outside chat (commit message, doc, issue, ticket, memory file).
