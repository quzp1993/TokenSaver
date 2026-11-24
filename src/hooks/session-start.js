#!/usr/bin/env node
// token-saver — SessionStart / SubagentStart hook
// Injects the 3-lever ruleset as session context so the rules stay active
// without the user invoking the skill. Fail-safe: any error = no injection.

let input = '';
process.stdin.on('data', (d) => (input += d));
process.stdin.on('end', () => {
  let event;
  try {
    const data = JSON.parse(input || '{}');
    event = data.hook_event_name === 'SubagentStart' ? 'SubagentStart' : 'SessionStart';
  } catch {
    process.exit(0);
  }

  const ruleset = [
    'TOKENSAVER RULES (always on):',
    'OUTPUT: answer first. Code/SQL/shell = code block only, zero prose. Facts = comma list or key:value, no bullets, no arrows, no emoji. Drop articles and connectors, never drop negations (not/never/no/only/except/未/勿/不能). Numbers and paths verbatim.',
    'INPUT: batch related commands. Prefer compact flags (git status --short, git diff --stat, git log --oneline -n). Pipe noisy output down (| tail -n 20, 2>&1 | tail). Grep instead of cat. Read log tails only.',
    'CONTEXT: keep CLAUDE.md to one-line pointers. Offload long references to files read on demand. Cite paths, do not re-paste.',
    'Break to full sentences for security, irreversible actions, multi-step order, or ambiguity.'
  ].join('\n');

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: event, additionalContext: ruleset },
  }));
});
