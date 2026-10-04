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

## Известные проблемы (найдено 2026-10-04)

1. **Кракозябры вместо русского текста.** Русские строки в `reels_mvp.py` испорчены двойной перекодировкой (UTF-8 прочитан как cp1251 и сохранён снова). Пользователь в Telegram увидит «РђРЅР°Р»РёР·...» вместо «Анализ...». Чинится обратным преобразованием `s.encode('cp1251').decode('utf-8')`, но часть символов (эмодзи) могла потеряться — проверять вручную.
2. **Mock-режим Instagram не срабатывает.** Значение по умолчанию `INSTAGRAM_ACCESS_TOKEN` = `"MOCK_INSTAGRAM_TOKEN"`, а проверки сравнивают с `"MOCK_ACCESS_TOKEN"`. Без настоящего токена бот пойдёт в реальный Graph API с фейковым токеном и получит ошибку публикации.
3. Проверка готовости контейнера делается один раз, без ожидания — реальное видео не успеет обработаться (`Timeout encoding video`).
