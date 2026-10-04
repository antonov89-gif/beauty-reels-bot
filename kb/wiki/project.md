# Проект: beauty-reels-bot

Telegram-бот на aiogram 3 — панель управления UGC-креатора косметики. Один файл `reels_mvp.py` (~650 строк).

## Конвейер

Конкурент → идеи → черновик сценария → одобрение в Telegram → публикация Reels в Instagram → аналитика.

Агенты (`MultiAgentSwarm`): Competitor → Strategy → Script → QA. Сейчас **все заглушки**: возвращают захардкоженные тексты, LLM (`call_llm`, OpenAI gpt-4o) нигде не вызывается.

Публикация (`InstagramPublishingAgent`): Instagram Graph API v20.0 — создать контейнер REELS → проверить статус → `media_publish`.

## Данные

SQLite `reels_automation.db`, таблицы: `competitors`, `ideas`, `drafts` (title/hook/body/cta/visual_prompt/audio_prompt, статус), `analytics`.
При старте `seed_beauty_ugc_database()` **удаляет все drafts** и заливает демо-сценарии.

## Запуск

Переменные окружения: `TELEGRAM_BOT_TOKEN` (обязательно), `OPENAI_API_KEY`, `INSTAGRAM_BUSINESS_ACCOUNT_ID`, `INSTAGRAM_ACCESS_TOKEN`, `PORT` (по умолчанию 8080).
Параллельно поднимается веб-сервер на `PORT` для health-check Render.

## Исправлено (2026-10-04)

1. **Кракозябры вместо русского текста** — строки были испорчены двойной перекодировкой (UTF-8 → cp1251, неразрывный пробел превращён в обычный). Восстановлено обратным преобразованием, эмодзи и кнопки целы.
2. **Mock-режим Instagram** — проверки сравнивали токен с `"MOCK_ACCESS_TOKEN"`, а дефолт `"MOCK_INSTAGRAM_TOKEN"`. Теперь без токена публикация симулируется.
3. **Ожидание обработки видео** — добавлен `InstagramPublishingAgent.wait_until_ready()`: опрос статуса контейнера каждые 10 с, до 5 минут.

## Осталось

- Агенты (`MultiAgentSwarm`) — заглушки с захардкоженными текстами, `call_llm` не используется.
- `seed_beauty_ugc_database()` при каждом старте удаляет все черновики.
