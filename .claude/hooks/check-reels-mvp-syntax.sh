#!/bin/bash
# PostToolUse guard: catch a syntax error in reels_mvp.py right after an edit,
# not at the next bot restart. reels_mvp.py is the bot's only source file and
# has a documented mojibake/encoding history (see README.md).
cd "$CLAUDE_PROJECT_DIR" || exit 0
[ -f reels_mvp.py ] || exit 0
err=$(python3 -c "import ast; ast.parse(open('reels_mvp.py', encoding='utf-8').read())" 2>&1)
if [ -n "$err" ]; then
  echo "SYNTAX ERROR in reels_mvp.py:" >&2
  echo "$err" >&2
  exit 2
fi
exit 0
