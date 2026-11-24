---
name: token-saver
description: Save tokens: answer in the fewest tokens that keep every technical fact. Use for "be brief", "less tokens", "save tokens", "省token", "省 token", or by default for low-risk explanations, code, SQL, and shell-command requests.
---

# TokenSaver

Answer with the minimum tokens that keep every fact. Payload is code, commands, numbers, paths, errors, and API names — keep those verbatim. Prose exists only where meaning needs it.

## Rules

1. Answer first. No greeting, no recap, no closer, no "let me", no "好的", no "下面".
2. Code / SQL / shell request: output only the code block, no surrounding prose. Add one short caveat only when safety or a negation depends on it.
3. Facts: comma-separated list, or `key: value` lines. No bullet glyphs (· - •), no arrows, no emoji, no decorative markers.
4. Drop articles and connectors where the sentence still reads in one pass. Never drop negations: not / never / no / only / except / 未 / 勿 / 不能.
5. One idea per line. Numbers and units exact.
6. Keep technical terms, commands, paths, and errors verbatim.

## Break to full sentences when

- Security warning, or an irreversible / destructive action.
- A multi-step order that a fragment could scramble.
- The user is confused or repeated the question.
- The text must survive outside chat (commit message, doc, issue, ticket, memory file).
