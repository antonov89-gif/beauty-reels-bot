#!/bin/bash
# Installs HyperFrames (HTML -> video renderer) and its render dependencies
# in Claude Code on the web sessions. Idempotent; safe to run on every start.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

HF_VERSION="0.8.68"

if ! command -v hyperframes >/dev/null 2>&1 || [ "$(hyperframes --version 2>/dev/null)" != "$HF_VERSION" ]; then
  npm install -g "hyperframes@${HF_VERSION}" >/dev/null 2>&1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  (apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg) >/dev/null 2>&1 || true
fi

hyperframes browser ensure >/dev/null 2>&1 || true

if [ ! -d "$HOME/.claude/skills/hyperframes" ]; then
  HYPERFRAMES_NO_TELEMETRY=1 hyperframes skills update >/dev/null 2>&1 || true
fi
