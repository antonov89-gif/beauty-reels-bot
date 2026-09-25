#!/bin/bash
# Color-coded context-usage progress bar for Claude Code's status line.
# Reads the session JSON Claude Code pipes on stdin (see statusLine docs).
input=$(cat)

model=$(echo "$input" | jq -r '.model.display_name // "?"')
pct=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
[ -z "$pct" ] && pct=0

branch=$(git branch --show-current 2>/dev/null)

# 20-segment bar, filled proportionally to pct.
bar_width=20
filled=$(( pct * bar_width / 100 ))
[ "$filled" -gt "$bar_width" ] && filled=$bar_width
empty=$(( bar_width - filled ))

# Color by threshold: green < 50%, yellow 50-79%, red >= 80%.
if [ "$pct" -ge 80 ]; then color="\033[31m"    # red
elif [ "$pct" -ge 50 ]; then color="\033[33m"  # yellow
else color="\033[32m"; fi                       # green
reset="\033[0m"

bar=$(printf '█%.0s' $(seq 1 $filled) 2>/dev/null)
gap=$(printf '░%.0s' $(seq 1 $empty) 2>/dev/null)

# %b (not %s) so \033 in $color/$reset is interpreted as an escape, not literal text.
printf "[%s] %b%s%s %s%%%b" "$model" "$color" "$bar" "$gap" "$pct" "$reset"
[ -n "$branch" ] && printf " | %s" "$branch"
printf "\n"
