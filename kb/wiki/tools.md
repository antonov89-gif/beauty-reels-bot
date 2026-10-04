# Инструменты Claude Code для проекта

## Установлено

- **Agent Reach** — скилл в `.claude/skills/agent-reach/` (в git). Доступ к вебу, YouTube, GitHub, RSS; LinkedIn/Instagram/Reddit/Twitter требуют cookies. Сам CLI `agent-reach` надо ставить в каждой новой облачной сессии: `pip install https://github.com/Panniantong/agent-reach/archive/main.zip`.
- **ECC (Everything Claude Code)** `ecc@ecc` и **claude-code-setup** — плагины, ставились в облачный контейнер (scope: user), **не сохраняются** между сессиями. Локально: `/plugin marketplace add https://github.com/affaan-m/ECC`, `/plugin install ecc@ecc`; `claude-code-setup` — из официального каталога Anthropic.
- **Context7 MCP** — свежая документация библиотек (aiogram, OpenAI, Instagram Graph API). Подключён в `.mcp.json` (remote, `https://mcp.context7.com/mcp`). В облаке нужен домен `mcp.context7.com` в Allowed domains окружения.
- **Субагенты из Agency Agents** (github.com/msitarzewski/agency-agents, MIT) в `.claude/agents/`: Instagram Curator, TikTok Strategist, Short Video Editing Coach, Content Creator. Остальные ~225 агентов библиотеки не ставим — шум в выборе агентов. Их роли пригодятся и как системные промпты для `call_llm` в боте.
- **Правила Карпати** (github.com/forrestchang/andrej-karpathy-skills) — добавлены в `CLAUDE.md`: думать до кода, простота, точечные правки, проверка результата.
- **База знаний `kb/`** (этот wiki) — паттерн raw / wiki / output, совместим с Obsidian.

## Отложено / не ставим

- **OpenMontage** (ИИ-видеопродакшн, github.com/calesthio/OpenMontage) — полезен для генерации рилсов, но ставить локально: в облаке YouTube и сервисы генерации заблокированы сетью.
- **claude-mem**, **Agent Skills** (Addy Osmani), **find-skills** — дублируют ECC.
- **AnyDoc** — не нужен, встроенные скиллы читают docx/xlsx/pptx.
- **Firecrawl MCP** — нужен платный ключ, чтение сайтов уже даёт Agent Reach.
- **Playwright MCP** — у бота нет веб-интерфейса.
- **OmniRoute** — прокси, отправляет код сторонним бесплатным моделям. Не ставим.
- **Headroom** — прокси-сжатие контекста, экономия ~15–20%. Только локально, по желанию.

## Ограничения облачной сессии

- Сеть блокирует youtube.com — транскрипты видео получать через коннекторы vidIQ / Nexlev.
- Режим Auto блокирует запуск стороннего кода и правку `.claude/settings.json`.
