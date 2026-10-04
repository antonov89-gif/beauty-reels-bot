# Инструменты Claude Code для проекта

## Установлено

- **Agent Reach** — скилл в `.claude/skills/agent-reach/` (в git). Доступ к вебу, YouTube, GitHub, RSS; LinkedIn/Instagram/Reddit/Twitter требуют cookies. Сам CLI `agent-reach` надо ставить в каждой новой облачной сессии: `pip install https://github.com/Panniantong/agent-reach/archive/main.zip`.
- **ECC (Everything Claude Code)** `ecc@ecc` и **claude-code-setup** — плагины, ставились в облачный контейнер (scope: user), **не сохраняются** между сессиями. Локально: `/plugin marketplace add https://github.com/affaan-m/ECC`, `/plugin install ecc@ecc`; `claude-code-setup` — из официального каталога Anthropic.
- **Context7 MCP** — свежая документация библиотек (aiogram, OpenAI, Instagram Graph API). Подключён в `.mcp.json` (remote, `https://mcp.context7.com/mcp`). В облаке нужен домен `mcp.context7.com` в Allowed domains окружения.
- **Субагенты из Agency Agents** (github.com/msitarzewski/agency-agents, MIT) в `.claude/agents/`: Instagram Curator, TikTok Strategist, Short Video Editing Coach, Content Creator. Остальные ~225 агентов библиотеки не ставим — шум в выборе агентов. Их роли пригодятся и как системные промпты для `call_llm` в боте.
- **Правила Карпати** (github.com/forrestchang/andrej-karpathy-skills) — добавлены в `CLAUDE.md`: думать до кода, простота, точечные правки, проверка результата.
- **Ponytail** (`ponytail@ponytail`), **Agent Skills** (`agent-skills@addy-agent-skills`) — плагины, поставлены по решению владельца проекта (2026-10-04). В облаке не сохраняются между сессиями.
- **Graphify** — `pip install graphifyy` + `graphify install --platform claude`; граф знаний по коду (`/graphify .`). Для проекта на один файл пока малополезен.
- **OmniRoute** v3.8.48 (`npm i -g omniroute`) — установлен, но **не запущен и не подключён**: если направить Claude Code на него (`ANTHROPIC_BASE_URL`), запросы и код уйдут сторонним бесплатным провайдерам и вместо Claude будут отвечать другие модели. Включать осознанно и только на своём компьютере.
- **Playwright MCP** и **Firecrawl MCP** — добавлены в `.mcp.json` по решению владельца (2026-10-04). Playwright без ключей (`@playwright/mcp`); Firecrawl требует `FIRECRAWL_API_KEY` в окружении, без него не стартует. Оба при первом запуске Claude Code ждут подтверждения (`/mcp`). У бота нет веб-интерфейса, так что практической пользы мало.
- **База знаний `kb/`** (этот wiki) — паттерн raw / wiki / output, совместим с Obsidian.

## Отложено / не ставим

- **OpenMontage** (ИИ-видеопродакшн, github.com/calesthio/OpenMontage) — полезен для генерации рилсов, но ставить локально: в облаке YouTube и сервисы генерации заблокированы сетью.
- **claude-mem**, **find-skills** — дублируют ECC.
- **AnyDoc** — не нужен, встроенные скиллы читают docx/xlsx/pptx.
- **Strix** — ИИ-пентестер веб-приложений (нужны Docker и ключ LLM); у бота нет веб-интерфейса, только health-check.
- **Headroom** — прокси-сжатие контекста, экономия ~15–20%. Только локально, по желанию.

## Ограничения облачной сессии

- Сеть блокирует youtube.com — транскрипты видео получать через коннекторы vidIQ / Nexlev.
- Режим Auto блокирует запуск стороннего кода и правку `.claude/settings.json`.
