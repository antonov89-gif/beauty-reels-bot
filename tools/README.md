# tools/

Security/dev tooling installed for use *on this repo*, not part of the bot.

## SkillSpector (NVIDIA)

Official security scanner for Claude Code / Codex / MCP skills:
https://github.com/NVIDIA/SkillSpector (Apache-2.0)

Not vendored into this repo (it's a standalone pip package, not a skill/library
this project imports). Installed into an isolated venv since it requires
Python >=3.12 and this environment's default python3 is 3.11:

```bash
python3.12 -m venv /opt/skillspector-venv
/opt/skillspector-venv/bin/pip install skillspector
```

Usage:

```bash
/opt/skillspector-venv/bin/skillspector scan <path-or-git-url> --no-llm
```

**Caveat found while testing on this repo's own `.claude/skills/`:** without
an LLM API key (`--no-llm`, static analysis only), it produces real false
positives on any skill whose *subject matter* is security or prompt
engineering -- e.g. it flagged `security-and-hardening` (a skill that teaches
threat modeling) as CRITICAL for containing the example phrase "disable
security" in its own documentation, and `prompt-master` for discussing
"system prompt" as a prompt-engineering concept. Manually verified both are
false positives by reading the flagged text. For trustworthy verdicts, run
with an LLM provider configured (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or
`SKILLSPECTOR_PROVIDER=ollama` for local models) rather than `--no-llm`.

## ScrapeGraphAI

Official pip package, real project (`ScrapeGraphAI/Scrapegraph-ai` on GitHub).
Video claimed "30k+ stars" -- actual count is in the low thousands, so that
figure was inflated, but the project itself is legitimate.

Installed into its own venv (needs its own dependency set -- langchain,
playwright, etc. -- separate from the bot's requirements.txt):

```bash
python3.12 -m venv /opt/scrapegraphai-venv
/opt/scrapegraphai-venv/bin/pip install scrapegraphai
```

Verified: `import scrapegraphai` works, version 2.2.4. Needs an LLM API key
(OpenAI/Anthropic/etc.) to actually scrape anything -- none configured here.
Not wired into the bot; nothing in reels_mvp.py currently needs web scraping.

## claude-automation-recommender (official Anthropic)

Installed as a Claude Code skill at `.claude/skills/claude-automation-recommender/`.
From `anthropics/claude-plugins-official`, the `claude-code-setup` plugin.
Read-only: analyzes a repo and recommends MCP servers, skills, hooks,
subagents, and slash commands worth adding -- doesn't modify anything itself.

## google/skills (verified, not installed)

Real official Google repo (Apache-2.0, github.com/google/skills) -- ~12.2k
GitHub stars (the video's "80k+" claim is inflated). 100+ skills for BigQuery,
GKE, Cloud Run, Firebase, Google Ads, etc. Not installed here: none of it is
relevant to this Telegram bot's stack. Ask if a specific skill from it is
ever needed.

## SkillUI

Installed globally via npm (`npm install -g skillui@1.3.4`, from the real
author amaancoderx/npxskillui, verified by matching package.json's
repository field). Reverse-engineers a design system (colors, fonts,
spacing, animations, components) from a live URL, git repo, or local
directory into a DESIGN.md + .skill package Claude Code reads
automatically. Pure static analysis -- no AI calls, no API keys.

Verified working: `skillui --url https://example.com` produced a valid
DESIGN.md and .skill package.

Not currently applicable to this repo (no web frontend to extract a design
system from) -- installed per explicit request for future use, e.g. if a
web dashboard is ever added to this project or used on an unrelated one.

## Ponytail

Vendored from https://github.com/DietrichGebert/ponytail (reviewed before
inclusion: MIT-licensed, all 4 hook scripts read line-by-line -- no network
calls, only local flag files, defensive try/catch everywhere, references
real GitHub issue numbers indicating an actively maintained project;
independently verified by JetBrains' blog with real, if smaller-than-
advertised, measured savings: -15% code / -10.3% cost across 80 paired
tasks).

"Lazy senior dev" mode: pushes the agent toward YAGNI, stdlib-first,
no-unrequested-abstractions on every coding task.

Files installed at `.claude/plugins/ponytail/` (skills, hooks, commands),
but **the SessionStart/SubagentStart/UserPromptSubmit hooks that make it
auto-activate every session are NOT wired into `.claude/settings.json`** --
that edit was blocked by this environment's own "Self-Modification"
safety check (editing hook config that will auto-execute in future
sessions needs an explicit permission grant, not just chat approval).

The `skills/ponytail/SKILL.md` skill is still usable as an ordinary skill
(it triggers on "ponytail", "be lazy", "simplest solution", etc.) without
the hooks. To get always-on activation, a human needs to either:
- run this repo's own installer (`node scripts/...` from a real clone), or
- manually add the hook entries from `.claude/plugins/ponytail/hooks/claude-codex-hooks.json`
  to `.claude/settings.json` themselves (pointing CLAUDE_PLUGIN_ROOT at
  `.claude/plugins/ponytail`).

## OpenRouter (free LLM fallback for the bot)

`reels_mvp.py`'s `MultiAgentSwarm.call_llm` now falls back to OpenRouter
(openrouter.ai) when no real `OPENAI_API_KEY` is set but `OPENROUTER_API_KEY`
is. OpenRouter is OpenAI-request-compatible, so this is a small addition,
not a new SDK. Default free model: `meta-llama/llama-3.3-70b-instruct:free`
(override with `OPENROUTER_MODEL`, see openrouter.ai/models for other
`:free`-suffixed options like Qwen, Kimi/Moonshot, GLM).

Recommended over Bytez/NVIDIA NIM (also named in the same video) for this
use case: OpenAI-compatible API (minimal code change), the widest free-tier
model catalog, no enterprise account needed, better documented. Still
requires the user's own (free) OpenRouter API key -- none configured here.
