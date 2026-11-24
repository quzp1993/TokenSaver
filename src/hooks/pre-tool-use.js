#!/usr/bin/env node
// token-saver — PreToolUse hook (Bash)
// Conservative, lossless compaction of a small whitelist of commands.
// Anything else passes through untouched. Fail-safe: any error = allow unchanged.

let input = '';
process.stdin.on('data', (d) => (input += d));
process.stdin.on('end', () => {
  let data;
  try {
    data = JSON.parse(input || '{}');
  } catch {
    process.exit(0);
  }

  if (data.tool_name !== 'Bash') {
    process.exit(0);
  }

  const ti = data.tool_input || {};
  const cmd = (ti.command || '').trim();
  if (!cmd) process.exit(0);

  let next = cmd;
  if (cmd === 'git status') {
    next = 'git status --short';
  } else if (cmd === 'git log') {
    next = 'git log --oneline -n 30';
  }
  // No other rewrites on purpose: keep it safe and lossless.

  if (next === cmd) {
    process.exit(0); // unchanged: allow as-is
  }

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'allow',
      permissionDecisionReason: 'token-saver: compacted command',
      updatedInput: Object.assign({}, ti, { command: next }),
    },
  }));
});
