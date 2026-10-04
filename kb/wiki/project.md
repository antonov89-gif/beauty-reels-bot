# Проект: beauty-reels-bot

Telegram-бот на aiogram 3 — панель управления UGC-креатора косметики. Один файл `reels_mvp.py` (~650 строк).

## Конвейер

Конкурент → идеи → черновик сценария → одобрение в Telegram → публикация Reels в Instagram → аналитика.

Агенты (`MultiAgentSwarm`): Competitor → Strategy → Script → QA. Сейчас **все заглушки**: возвращают захардкоженные тексты, LLM (`call_llm`, OpenAI gpt-4o) нигде не вызывается.

Публикация (`InstagramPublishingAgent`): Instagram Graph API v20.0 — создать контейнер REELS → проверить статус → `media_publish`.

## Данные

SQLite `reels_automation.db`, таблицы: `competitors`, `ideas`, `drafts` (title/hook/body/cta/visual_prompt/audio_prompt, статус), `analytics`.
При старте `seed_beauty_ugc_database()` заливает демо-сценарии **только в пустую базу** (с 2026-10-04 черновики больше не стираются).

## Запуск

Переменные окружения: `TELEGRAM_BOT_TOKEN` (обязательно), `OPENAI_API_KEY`, `INSTAGRAM_BUSINESS_ACCOUNT_ID`, `INSTAGRAM_ACCESS_TOKEN`, `PORT` (по умолчанию 8080).
Параллельно поднимается веб-сервер на `PORT` для health-check Render.

## Исправлено (2026-10-04)

1. **Кракозябры вместо русского текста** — строки были испорчены двойной перекодировкой (UTF-8 → cp1251, неразрывный пробел превращён в обычный). Восстановлено обратным преобразованием, эмодзи и кнопки целы.
2. **Mock-режим Instagram** — проверки сравнивали токен с `"MOCK_ACCESS_TOKEN"`, а дефолт `"MOCK_INSTAGRAM_TOKEN"`. Теперь без токена публикация симулируется.
3. **Ожидание обработки видео** — добавлен `InstagramPublishingAgent.wait_until_ready()`: опрос статуса контейнера каждые 10 с, до 5 минут.

## Генерация черновиков (2026-10-04)

Кнопка «✨ Сгенерировать» (или `/generate`) → бот спрашивает тему → `generate_draft()`: Strategy → Script → QA через OpenAI (gpt-4o, JSON-режим) → черновик `PENDING_USER` с кнопками одобрения.
Промпты агентов — константы `*_SYSTEM_PROMPT` в начале `reels_mvp.py`.
Без `OPENAI_API_KEY` или при ошибке/не-JSON ответе агенты молча возвращают старые шаблоны (тема пользователя игнорируется).

## Доработка черновика (2026-10-04)

«🛠️ На доработку» → бот спрашивает замечание → `run_revision()` переписывает сценарий через OpenAI → QA → черновик обновляется на месте (`revision_feedback` = замечание, статус `PENDING_USER`).
Без OpenAI черновик не меняется, бот прямо сообщает об этом; замечание сохраняется.

## Осталось

- Агент конкурентов (`run_competitor_analysis`) — заглушка; план: Instagram Graph API Business Discovery.
- **SQLite на Render Free не переживает редеплой/рестарт** — файловая система эфемерная. Нужен Persistent Disk (платно) или внешняя БД (например, бесплатный Postgres: Neon/Supabase).
