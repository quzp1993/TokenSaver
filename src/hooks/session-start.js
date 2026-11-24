#!/usr/bin/env node
// token-saver — SessionStart / SubagentStart hook
// Injects the 3-lever ruleset and reports whether rtk (input engine) is present.
// Fail-safe: any error = no injection.

const { execSync } = require('child_process');

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

  let rtkStatus = 'rtk (input compression): unknown.';
  try {
    execSync('rtk --version', { stdio: 'ignore', timeout: 3000 });
    rtkStatus = 'rtk (input compression): active. Use `rtk <cmd>` for noisy output, `rtk bypass <cmd>` for full output.';
  } catch {
    rtkStatus = 'rtk (input compression): MISSING. Run `bash setup.sh` to install.';
  }

  const ruleset = [
    'TOKENSAVER RULES (always on):',
    'OUTPUT: answer first. Code/SQL/shell = code block only, zero prose. Facts = comma list or key:value, no bullets, no arrows, no emoji. Drop articles and connectors, never drop negations (not/never/no/only/except/未/勿/不能). Numbers and paths verbatim.',
    'INPUT: batch related commands. Prefer compact flags. Noisy command output runs through rtk. Grep instead of cat. Read log tails only.',
    rtkStatus,
    'CONTEXT: keep CLAUDE.md to one-line pointers. Offload long references to files read on demand. Cite paths, do not re-paste.',
    'Break to full sentences for security, irreversible actions, multi-step order, or ambiguity.'
  ].join('\n');

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: { hookEventName: event, additionalContext: ruleset },
  }));
});
