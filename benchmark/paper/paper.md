# TokenSaver: an orchestration pipeline for token-efficient coding agents

## Abstract

Large-language-model coding agents spend their token budget on three sinks: verbose
replies, raw command output, and bloated persistent context. Existing tools compress
one sink each. We present TokenSaver, a pipeline that orchestrates these tools under a
single install instead of reimplementing them: rtk compresses command output (input
lever), while TokenSaver's own skill and hooks compress replies (output lever) and keep
context lean (context lever). Across 100 questions spanning ten task categories,
TokenSaver reduced answer tokens by 89.2% relative to a verbatim baseline (40,654 to
4,391 tokens) while raising key-information retention from 0.662 to 0.825. A reference
session combining all three levers reduced total token consumption by 99.2% (146,607 to
1,189 tokens). These results show that terseness and information retention are not in
tension: concise output preserves more key facts than verbose prose. TokenSaver is
released as an open-source Claude Code plugin.

## Main

**Three levers, one pipeline.** Token cost in an agentic coding session concentrates in
three places. The *output* lever is the assistant's reply; verbose prose, greetings, and
restated explanations are charged to the user without carrying information. The *input*
lever is command output — build logs, `find`, `git log` — which enters the context before
the model reads it. The *context* lever is the persistent instructions and documentation
loaded at every session start. TokenSaver treats these as three separate engineering
problems and assigns each to the tool best suited for it (Fig. 2): rtk for input
compression, a terse-answer skill for output, and a pointer-based layout plus a
SessionStart hook for context.

**Output compression preserves, and even improves, information.** We benchmarked the
output lever on 100 questions across ten categories (concept, code, SQL, shell, git,
regex, debugging, comparison, summarization, statistics). Each question was answered by
the same model under three system prompts: a verbatim baseline, a "caveman" terse style,
and the TokenSaver style. Answer length was measured with a cl100k_base tokenizer on the
visible reply, and retention was scored as the fraction of pre-specified key-information
items present in the answer. TokenSaver reduced total answer tokens by 89.2% relative to
baseline (Fig. 1a, 1c). Strikingly, retention *rose* from 0.662 (baseline) to 0.825
(TokenSaver) (Fig. 1b): verbose answers bury or paraphrase key facts, whereas terse
instructions force the model to state them directly. This reproduces, in a coding-agent
setting, the reported accuracy benefit of concise output.

**Combined savings across levers.** In a reference session — 10 question-answer pairs, a
mix of four command types, and one session start — the three levers together reduced
token consumption from 146,607 to 1,189 tokens, a 99.2% reduction (Fig. 2). The input
lever dominates in absolute terms (144,256 to 414 tokens), because raw `find` and log
output can be orders of magnitude larger than any reply. The output lever contributes a
proportional −70% on the reply itself, and the context lever replaces a multi-hundred-token
CLAUDE.md with a five-token pointer plus a fixed 193-token ruleset injection.

## Methods

**Benchmark.** One hundred questions were written across ten categories (ten per
category), each annotated with 2–4 key-information items as retention ground truth. Each
question was submitted to deepseek-v4-pro through an Anthropic-compatible API three times,
once per system prompt, with the output style (verbatim, caveman, TokenSaver) as the only
varying instruction; language was fixed to Simplified Chinese. Visible reply text was
extracted from the response blocks, and answer length was counted with the cl100k_base
tokenizer. Retention was computed per answer as the fraction of key-information substrings
present (case-insensitive). The three-lever reference session used the ten-question output
pilot (1,644 to 479 tokens), four real command outputs for the input lever, and measured
persistent-context files for the context lever; the full 100-question result supersedes
the pilot for the output-lever claim.

**System.** TokenSaver is a Claude Code plugin: a SessionStart/SubagentStart hook injects
the three-lever ruleset each session, a PreToolUse hook applies a lossless whitelist of
command rewrites (`git status --short`, `git log --oneline -n 30`), and a setup script
installs rtk and registers its hook. The design is an orchestrator, not a reimplementation:
input compression is delegated to rtk rather than duplicated.

## Discussion

TokenSaver's central observation is that token saving should be organized by *where*
tokens are spent, not by a single compression trick. The three levers are independent and
compose multiplicatively; the largest wins come from the input lever, which no
answer-shortening skill can address. A second observation is that conciseness and fidelity
are aligned rather than opposed, at least for factual question-answering: the terse
strategies preserved more key information than the verbose baseline.

Limitations bound these claims. The benchmark uses a single model and a single endpoint;
retention is a substring-presence proxy, not a semantic-equivalence measure; and the input
lever's performance is inherited from rtk rather than contributed by TokenSaver. We also
did not measure thinking/reasoning tokens, which are style-independent and therefore
outside the output lever's effect. Future work should extend the benchmark to multiple
models, add a semantic retention scorer, and measure end-to-end cost on real development
sessions rather than synthetic question-answer pairs.

## Figures

**Fig. 1 | Output lever on 100 questions.** (a) Per-answer token distribution (log scale)
for baseline, caveman, and TokenSaver. (b) Mean key-information retention (± s.e.m.).
(c) Total answer tokens (log scale), with savings relative to baseline.

**Fig. 2 | Three-lever integration.** Tokens (log scale) for the output, input, context,
and combined levers, baseline versus TokenSaver. Percentages denote per-lever reduction.
