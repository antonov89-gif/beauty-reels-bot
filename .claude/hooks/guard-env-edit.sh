#!/bin/bash
# PreToolUse guard: .env files hold real secrets (OpenRouter, ElevenLabs,
# Instagram token). Block silent Edit/Write to any .env* file except the
# .example templates, forcing an explicit confirmation prompt instead.
input=$(cat)
path=$(echo "$input" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))" 2>/dev/null)
case "$path" in
  *.env.example|*.env.sample) exit 0 ;;
  *.env|*.env.*)
    echo "Blocked: edit to $path holds real secrets. Confirm explicitly if this is intentional." >&2
    exit 2
    ;;
esac
exit 0
