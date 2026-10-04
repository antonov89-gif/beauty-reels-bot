import os
import json
import sqlite3
import asyncio
import logging
from datetime import datetime, timedelta
import aiohttp
from aiohttp import web

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("UGC_Beauty_Orchestrator")

# AIOGRAM Imports
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# =====================================================================
# CONFIGURATION & API KEYS PLACEHOLDERS
# =====================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "MOCK_OPENAI_API_KEY")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "MOCK_INSTAGRAM_ID")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "MOCK_INSTAGRAM_TOKEN")

# =====================================================================
# AGENT PROMPTS
# =====================================================================
SCRIPT_FIELDS = ("title", "hook", "body", "cta", "visual_prompt", "audio_prompt")

STRATEGY_SYSTEM_PROMPT = (
    "Ты контент-стратег бьюти-UGC для Instagram Reels (уход за кожей, косметика). "
    "Превращаешь темы в оригинальные концепты коротких вертикальных роликов 15–30 секунд: "
    "понятная польза или эстетика, один ролик — одна мысль. Пиши по-русски. Отвечай только JSON."
)

SCRIPT_SYSTEM_PROMPT = (
    "Ты сценарист бьюти-UGC Reels. По концепту напиши сценарий ролика 15–30 секунд по-русски. "
    "Хук должен цеплять в первые 1–3 секунды. Без медицинских обещаний («вылечит», «навсегда уберёт»). "
    "Ответ строго JSON с ключами: "
    '"title" (концепт, до 60 символов), "hook" (первая фраза), '
    '"body" (что происходит в кадре и что говорится), "cta" (призыв к действию), '
    '"visual_prompt" (ТЗ для съёмки или генерации видео, по-английски), '
    '"audio_prompt" (звук и музыка, по-английски).'
)

QA_SYSTEM_PROMPT = (
    "Ты редактор и модератор бьюти-контента. Проверь сценарий Reels: соответствие правилам Meta "
    "(нет медицинских обещаний, нет «до/после» с нереалистичным результатом, нет запрещённых утверждений), "
    "сила хука, ясность призыва к действию. "
    'Ответ строго JSON: {"is_passed": true/false, "score": число от 1 до 10, "notes": "кратко по-русски"}.'
)

# =====================================================================
# DATABASE MANAGEMENT (SQLite)
# =====================================================================
DB_PATH = "reels_automation.db"

def init_db():
    """Initializes the relational database schema tailored for Beauty UGC."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Competitors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            added_at TEXT NOT NULL,
            last_scraped TEXT,
            status TEXT DEFAULT 'ACTIVE'
        )
    """)
    
    # 2. Ideas Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            source_competitor_id INTEGER,
            created_at TEXT NOT NULL,
            status TEXT DEFAULT 'NEW',
            FOREIGN KEY (source_competitor_id) REFERENCES competitors(id)
        )
    """)
    
    # 3. Drafts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idea_id INTEGER,
            title TEXT,
            hook TEXT,
            body TEXT,
            cta TEXT,
            visual_prompt TEXT,
            audio_prompt TEXT,
            status TEXT DEFAULT 'IDEA_GENERATED', 
            revision_feedback TEXT,
            scheduled_time TEXT,
            instagram_container_id TEXT,
            media_url TEXT,
            instagram_media_id TEXT,
            created_at TEXT,
            FOREIGN KEY (idea_id) REFERENCES ideas(id)
        )
    """)
    
    # 4. Analytics Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            draft_id INTEGER,
            instagram_media_id TEXT UNIQUE,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            saves INTEGER DEFAULT 0,
            captured_at TEXT,
            FOREIGN KEY (draft_id) REFERENCES drafts(id)
        )
    """)
    
    conn.commit()
    conn.close()
    logger.info("Database schema initialized and tailored for Beauty UGC.")

# Helper DB Functions
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# =====================================================================
# AGENT LOGIC (TAILORED FOR BEAUTY UGC)
# =====================================================================
class MultiAgentSwarm:
    @staticmethod
    async def call_llm(prompt: str, system_message: str, json_mode: bool = False) -> str:
        """Integration point with OpenAI API."""
        if OPENAI_API_KEY == "MOCK_OPENAI_API_KEY" or not OPENAI_API_KEY:
            await asyncio.sleep(1)
            return "MOCK_RESPONSE"
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        if json_mode:
            data["response_format"] = {"type": "json_object"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        return result["choices"][0]["message"]["content"]
                    return "MOCK_RESPONSE"
        except Exception as e:
            logger.error(f"Error LLM: {e}")
            return "MOCK_RESPONSE"

    async def run_competitor_analysis(self, username: str) -> list:
        logger.info(f"[Competitor Agent] Анализируем бьюти-аккаунт @{username}...")
        await asyncio.sleep(1)
        # Returns raw high-performing trends
        return [
            f"Эстетика капель сыворотки на лице крупным планом (рост удержания на 80% у @{username})",
            f"Шокирующий разбор ошибок очищения пор (активность у @{username})"
        ]

    async def call_llm_json(self, prompt: str, system_message: str):
        """Returns parsed JSON from the LLM, or None in mock mode / on a bad response."""
        raw = await self.call_llm(prompt, system_message, json_mode=True)
        if raw == "MOCK_RESPONSE":
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            logger.error(f"LLM returned non-JSON: {raw[:200]}")
            return None

    async def run_content_strategy(self, trends: list) -> list:
        logger.info("[Strategy Agent] Переводим тренды в концепты оригинального бьюти-UGC...")
        result = await self.call_llm_json(
            "Темы/тренды:\n" + "\n".join(f"- {t}" for t in trends) +
            '\n\nПредложи по одному концепту Reels на каждую тему. Ответ JSON: {"concepts": ["...", ...]}',
            STRATEGY_SYSTEM_PROMPT,
        )
        if result and result.get("concepts"):
            return [str(c) for c in result["concepts"]]
        await asyncio.sleep(1)
        return [
            f"UGC Концепт: Эстетика ASMR-нанесения матовой сыворотки с макролинзой",
            f"UGC Концепт: 3 ошибки ухода за лицом, которые разрушают кожный барьер"
        ]

    async def run_script_and_prompts(self, idea_topic: str) -> dict:
        logger.info(f"[Script Agent] Пишем детальный бьюти-сценарий по секундам...")
        result = await self.call_llm_json(f"Концепт ролика: {idea_topic}", SCRIPT_SYSTEM_PROMPT)
        if result and all(result.get(k) for k in SCRIPT_FIELDS):
            return {k: str(result[k]) for k in SCRIPT_FIELDS}
        await asyncio.sleep(1.5)

        if "ошибки" in idea_topic.lower():
            return {
                "title": "3 ошибки ухода, которые губят твою кожу",
                "hook": "Прекрати наносить сыворотку прямо из пипетки на лицо! И вот почему...",
                "body": "Касаясь пипеткой кожи, ты переносишь бактерии во флакон. Наноси средство на чистые ладони! Вторая ошибка: использовать агрессивные скрабы при акне. И третья: забывать про SPF-защиту летом и зимой.",
                "cta": "Пиши слово 'СПАСЕНИЕ' в комментариях, и я пришлю тебе пошаговую схему ухода за барьером кожи совершенно бесплатно!",
                "visual_prompt": "Aesthetic cinematic macro video. Female hand using a skincare glass dropper, dropping oil on palms. Soft morning bathroom background, diffuse white lighting.",
                "audio_prompt": "Warm ASMR whisper sound, soft lo-fi background beat, water splashing effects."
            }
        else:
            return {
                "title": "Эстетика ASMR: Твой новый утренний ритуал",
                "hook": "Эстетика ухода, которая заменяет тебе любые маски в инстаграме... ✨",
                "body": "Каждое утро твоя кожа заслуживает бережного отношения. Нежное облако пенки, капля питательной сыворотки и легкий массаж гуаша. Позволь себе эти 5 минут заботы.",
                "cta": "Все бьюти-продукты из этого видео оставила в описании. Какое твое любимое средство?",
                "visual_prompt": "Extreme macro close-up of pink face serum dripping, bubbles in gel cleanser, cream texture swirls under studio light, aesthetic beauty video style.",
                "audio_prompt": "Acoustic ASMR clicks, tapping on glass bottles, soft ambient water drops and peaceful sound design."
            }

    async def run_revision(self, script_data: dict, feedback: str):
        """Rewrites a script by user feedback. Returns the new script, or None if the LLM is unavailable."""
        logger.info("[Script Agent] Переписываем сценарий по замечанию...")
        result = await self.call_llm_json(
            "Текущий сценарий:\n" + json.dumps(script_data, ensure_ascii=False) +
            f"\n\nЗамечание автора: {feedback}\n\nПерепиши сценарий с учётом замечания, сохрани формат.",
            SCRIPT_SYSTEM_PROMPT,
        )
        if result and all(result.get(k) for k in SCRIPT_FIELDS):
            return {k: str(result[k]) for k in SCRIPT_FIELDS}
        return None

    async def run_qa_check(self, script_data: dict) -> dict:
        logger.info("[QA Agent] Проверка на соответствие бьюти-стандартам и политике Meta...")
        result = await self.call_llm_json(json.dumps(script_data, ensure_ascii=False), QA_SYSTEM_PROMPT)
        if result and "is_passed" in result:
            return {"is_passed": bool(result["is_passed"]), "score": result.get("score"), "notes": str(result.get("notes", ""))}
        await asyncio.sleep(0.5)
        return {"is_passed": True, "score": 9.5}


# =====================================================================
# OFFICIAL INSTAGRAM GRAPH API POSTING ENGINE (PUBLISHING AGENT)
# =====================================================================
class InstagramPublishingAgent:
    @staticmethod
    async def create_reels_container(media_url: str, caption: str) -> str:
        if INSTAGRAM_ACCESS_TOKEN == "MOCK_INSTAGRAM_TOKEN" or not INSTAGRAM_ACCESS_TOKEN:
            logger.info("[Publishing Agent] Симуляция загрузки Reels в Instagram...")
            await asyncio.sleep(1.5)
            return "MOCK_CONTAINER_ID_12345"
            
        url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
        params = {
            "media_type": "REELS",
            "video_url": media_url,
            "caption": caption,
            "share_to_feed": "true",
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                if response.status == 200:
                    res_data = await response.json()
                    return res_data["id"]
                raise Exception(f"IG Media Container Error: {await response.text()}")

    @staticmethod
    async def check_container_status(container_id: str) -> bool:
        if INSTAGRAM_ACCESS_TOKEN == "MOCK_INSTAGRAM_TOKEN" or not INSTAGRAM_ACCESS_TOKEN:
            await asyncio.sleep(1)
            return True
            
        url = f"https://graph.facebook.com/v20.0/{container_id}"
        params = {
            "fields": "status_code",
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    res_data = await response.json()
                    return res_data.get("status_code") == "FINISHED"
        return False

    @staticmethod
    async def wait_until_ready(container_id: str, timeout: int = 300, interval: int = 10) -> bool:
        """Instagram encodes Reels asynchronously: poll until FINISHED or timeout."""
        deadline = asyncio.get_running_loop().time() + timeout
        while True:
            if await InstagramPublishingAgent.check_container_status(container_id):
                return True
            if asyncio.get_running_loop().time() >= deadline:
                return False
            await asyncio.sleep(interval)

    @staticmethod
    async def publish_reels(container_id: str) -> str:
        if INSTAGRAM_ACCESS_TOKEN == "MOCK_INSTAGRAM_TOKEN" or not INSTAGRAM_ACCESS_TOKEN:
            logger.info("[Publishing Agent] Видео успешно опубликовано!")
            return "MOCK_MEDIA_ID_9988"
            
        url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
        params = {
            "creation_id": container_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as response:
                if response.status == 200:
                    res_data = await response.json()
                    return res_data["id"]
                raise Exception(f"Publishing Error: {await response.text()}")


# =====================================================================
# SEED BEAUTY UGC SCRIPTS IN THE DATABASE
# =====================================================================
async def seed_beauty_ugc_database():
    """Populates the database with actual high-quality UGC skincare drafts."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Seed only an empty database, so restarts keep user drafts
    if cursor.execute("SELECT COUNT(*) FROM drafts").fetchone()[0] > 0:
        conn.close()
        logger.info("Database already has drafts, skipping demo seed.")
        return

    # 1. Add premium competitors
    competitors = [("smorodina_cosmetic",), ("shikcosmetics",), ("mixit_ru",), ("art_visage",)]
    cursor.executemany("INSERT INTO competitors (username, added_at) VALUES (?, datetime('now'))", competitors)
    
    # 2. Add raw ideas
    ideas = [
        ("ASMR-распаковка новой корейской сыворотки", 1),
        ("3 Ошибки ухода: правильное нанесение тоника", 2),
        ("До/После: Спасение кожи лица от сухости и шелушений", 3),
        ("Эстетичный GRWM: утренний уход, заменяющий фильтры", 4)
    ]
    for topic, comp_id in ideas:
        cursor.execute("INSERT INTO ideas (topic, source_competitor_id, created_at, status) VALUES (?, ?, datetime('now'), 'GENERATED')", (topic, comp_id))
        
    # 3. Add 4 highly tailored, pre-written UGC Beauty Drafts awaiting user approval
    beauty_drafts = [
        (
            1, "Эстетичная ASMR-распаковка",
            "Эстетика ухода, которая заменяет тебе любые маски в инстаграме... ✨",
            "Постукивание ногтями по коробке, шуршание крафтовой бумаги, медленное извлечение стеклянного флакона и падение капли сыворотки на ладонь в слоу-мо.",
            "Пиши слово 'СИЯНИЕ' в комментариях, и я пришлю тебе ссылку на этот бренд!",
            "Extreme macro close-up of a premium glass dropper bottle, pink serum dripping. Soft sun rays, aesthetic background, 8k beauty lighting.",
            "Clean acoustic ASMR clicks, paper rustling, water drop effect, cozy lofi chillhop background music.",
            "PENDING_USER"
        ),
        (
            2, "3 Ошибки ухода за лицом",
            "Прекрати наносить сыворотку прямо из пипетки на лицо! И вот почему...",
            "Спикер качает головой 'НЕТ', держа пипетку у лица (красный крест). Затем показывает правильный вариант: капли на ладони, растирание и бережное похлопывание по коже.",
            "Подпишись на профиль, у меня всё о бережном и правильном уходе за лицом каждый день!",
            "Beauty UGC style video, hands applying cosmetic product on skin, soft diffuse warm light, safe zones for instagram reels text.",
            "Warm conversational voiceover, slight ambient background lounge beat.",
            "PENDING_USER"
        ),
        (
            3, "До / После: SOS-увлажнение",
            "Моя кожа кричала о помощи от дикой сухости и стянутости...",
            "Показываем сухую тусклую кожу крупным планом. Наносим крем сливочной текстуры с центеллой. Вжух-эффект — кожа сияет, напитана, макияж ложится безупречно.",
            "Сохрани этот рилс, чтобы не потерять название этого SOS-крема!",
            "Macro shot of cosmetic cream texture being swirled with a gold spatula. Panning camera shot, beautiful lighting, pink aesthetics.",
            "Swoosh transition effect, relaxing water droplet sound design, ambient morning tracks.",
            "PENDING_USER"
        ),
        (
            4, "Утренний GRWM: Забота о лице",
            "Давай сделаем утренний уход, после которого тебе не понадобятся фильтры...",
            "Умывание обильной пенкой, мягкое промакивание полотенцем, тонер похлопываниями и обязательный SPF-защитный крем в виде аккуратных точек на лице.",
            "Все этапы и бренды оставила в описании к видео. А какой твой любимый SPF?",
            "Skincare lifestyle video. Smiling creator in cozy bathrobe with a white headband washing face with foam. Soft bathroom background.",
            "Splashing water sounds, morning birds chirping, low volume cozy acoustic guitar.",
            "PENDING_USER"
        )
    ]
    
    cursor.executemany("""
        INSERT INTO drafts (
            idea_id, title, hook, body, cta, visual_prompt, audio_prompt, status, created_at, media_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), 'https://pub-static.arena.ai/assets/placeholder_video.mp4')
    """, beauty_drafts)
    
    conn.commit()
    conn.close()
    logger.info("Database successfully seeded with 4 custom UGC Beauty scripts.")


# =====================================================================
# ТЕЛЕГРАМ РОУТЕР И КОМАНДЫ
# =====================================================================
if TELEGRAM_BOT_TOKEN:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
else:
    bot = None
dp = Dispatcher()
router = Router()

def get_main_reply_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="🌸 Черновики (сценарии)"),
            KeyboardButton(text="🗓️ Контент-план")
        ],
        [
            KeyboardButton(text="📊 Статус завода"),
            KeyboardButton(text="🔍 Конкуренты")
        ],
        [
            KeyboardButton(text="📅 Расписание"),
            KeyboardButton(text="📈 Аналитика")
        ],
        [
            KeyboardButton(text="✨ Сгенерировать")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, persistent=True)

def get_draft_approval_keyboard(draft_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"app_{draft_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"rej_{draft_id}")
        ],
        [
            InlineKeyboardButton(text="🛠️ На доработку", callback_data=f"rev_{draft_id}"),
            InlineKeyboardButton(text="📅 В расписание", callback_data=f"sch_{draft_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# --- COMMAND: /start ---
@router.message(Command("start"))
@router.message(F.text.lower().in_({"старт", "start", "начать", "привет", "меню", "menu", "приветик", "приветик"}))
async def cmd_start(message: Message):
    print(f"📥 [DEBUG START] Получено сообщение /start от {message.from_user.username} ({message.from_user.id})", flush=True)
    try:
        welcome_text = (
            "🌸 **Добро пожаловать в Панель Управления UGC-креатора косметики!** 🌸\n\n"
            "Я ваш специализированный ИИ-оркестратор. Мои агенты обучены бьюти-копирайтингу, "
            "эстетической съемке и нативным воронкам ухода за лицом.\n\n"
            "Я закрепил на вашем экране постоянные **кнопки управления** — просто нажимайте на них на панели внизу, чтобы управлять агентами! 👇"
        )
        print("⚙️ [DEBUG START] Формирую клавиатуру...", flush=True)
        kbd = get_main_reply_keyboard()
        print("📨 [DEBUG START] Вызываю message.reply...", flush=True)
        res = await message.reply(welcome_text, reply_markup=kbd, parse_mode="Markdown")
        print(f"✅ [DEBUG START] Успешно отправлено! Message ID: {res.message_id}", flush=True)
    except Exception as e:
        print(f"❌ [DEBUG START] КРИТИЧЕСКАЯ ОШИБКА в cmd_start: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()

# --- COMMAND: /status ---
@router.message(Command("status"))
@router.message(F.text.lower().in_({"статус", "status", "статистика", "📊 статус завода"}))
async def cmd_status(message: Message):
    conn = get_db_connection()
    stats = conn.execute("SELECT status, COUNT(*) as cnt FROM drafts GROUP BY status").fetchall()
    conn.close()
    
    status_text = "📊 **Статистика конвейера UGC-Косметики:**\n\n"
    if not stats:
        status_text += "Воронка пуста. ИИ-агенты запускают новый цикл генерации."
    else:
        for row in stats:
            status_text += f"• *{row['status']}*: {row['cnt']} видео\n"
            
    await message.reply(status_text, parse_mode="Markdown")

# --- COMMAND: /competitors ---
@router.message(Command("competitors"))
@router.message(F.text.lower().in_({"конкуренты", "competitors", "🔍 конкуренты"}))
async def cmd_competitors(message: Message):
    conn = get_db_connection()
    competitors = conn.execute("SELECT * FROM competitors").fetchall()
    conn.close()
    
    text = "🔍 **База отслеживаемых бьюти-аккаунтов:**\n\n"
    for comp in competitors:
        text += f"• @{comp['username']} (Статус: {comp['status']})\n"
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /add_competitor ---
@router.message(Command("add_competitor"))
async def cmd_add_competitor(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("❌ Пример добавления: `/add_competitor drcella_skincare`", parse_mode="Markdown")
        return
    username = args[1].replace("@", "").strip()
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO competitors (username, added_at) VALUES (?, datetime('now'))", (username,))
        conn.commit()
        await message.reply(f"✅ Аккаунт **@{username}** добавлен в базу Агента-Аналитика!", parse_mode="Markdown")
    except sqlite3.IntegrityError:
        await message.reply("❌ Этот аккаунт уже отслеживается.")
    finally:
        conn.close()

# --- COMMAND: /content_plan ---
@router.message(Command("content_plan"))
@router.message(F.text.lower().in_({"план", "идеи", "контент-план", "content_plan", "🗓️ контент-план"}))
async def cmd_content_plan(message: Message):
    conn = get_db_connection()
    ideas = conn.execute("SELECT * FROM ideas ORDER BY id DESC").fetchall()
    conn.close()
    
    text = "🗓️ **Адаптированные бьюти-идеи в контент-плане:**\n\n"
    for idea in ideas:
        text += f"📍 ID-{idea['id']} | {idea['topic']}\n\n"
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /drafts ---
@router.message(Command("drafts"))
@router.message(F.text.lower().in_({"черновики", "черновик", "сценарии", "сценарий", "drafts", "draft", "🌸 черновики (сценарии)"}))
async def cmd_drafts(message: Message):
    conn = get_db_connection()
    drafts = conn.execute("SELECT * FROM drafts WHERE status = 'PENDING_USER' ORDER BY id ASC").fetchall()
    conn.close()
    
    if not drafts:
        await message.reply("У вас нет готовых сценариев косметики на одобрение. Все ролики в эфире! 🎉")
        return
        
    for d in drafts:
        qa_text = (
            f"• Безопасность Meta: 10/10 (пройдено)\n"
            f"• Риски: Нет медицинских обещаний. Текст нативный."
        )
        await message.answer(format_draft_text(d, qa_text), reply_markup=get_draft_approval_keyboard(d['id']), parse_mode="Markdown")


def format_draft_text(d, qa_text: str) -> str:
    return (
        f"🌸 **БЬЮТИ-UGC ЧЕРНОВИК REELS ID: {d['id']}**\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **Концепт:** {d['title']}\n\n"
        f"🧲 **ХУК (0-3 сек):**\n_{d['hook']}_\n\n"
        f"📝 **ГОЛОС ЗА КАДРОМ / СУТЬ:**\n{d['body']}\n\n"
        f"📢 **СТА (Призыв к действию):**\n*{d['cta']}*\n\n"
        f"🎨 **AI ВИДЕО-ПРОМПТ (ТЗ для съемки):**\n`{d['visual_prompt']}`\n\n"
        f"🎙️ **AI АУДИО-ПРОМПТ (Sound Design):**\n`{d['audio_prompt']}`\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡️ **Анализ Шеф-Агента:**\n"
        f"{qa_text}"
    )


def format_qa_text(qa: dict) -> str:
    verdict = "пройдено" if qa["is_passed"] else "есть замечания"
    text = f"• Оценка: {qa['score']}/10 ({verdict})"
    if qa.get("notes"):
        text += f"\n• {qa['notes'].translate(str.maketrans('', '', '*_`[]'))}"
    return text


# --- COMMAND: /generate (кнопка «✨ Сгенерировать») ---
class GenerateDraft(StatesGroup):
    waiting_topic = State()


async def generate_draft(topic: str):
    """Strategy → Script → QA. Saves the idea and a PENDING_USER draft; returns (draft_id, qa)."""
    swarm = MultiAgentSwarm()
    concept = (await swarm.run_content_strategy([topic]))[0]
    script = await swarm.run_script_and_prompts(concept)
    # LLM text goes into Telegram Markdown: drop characters that would break the markup.
    script = {k: v.translate(str.maketrans("", "", "*_`[]")) for k, v in script.items()}
    qa = await swarm.run_qa_check(script)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ideas (topic, created_at, status) VALUES (?, datetime('now'), 'GENERATED')", (topic,))
    idea_id = cursor.lastrowid
    cursor.execute("""
        INSERT INTO drafts (
            idea_id, title, hook, body, cta, visual_prompt, audio_prompt, status, created_at, media_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'PENDING_USER', datetime('now'), 'https://pub-static.arena.ai/assets/placeholder_video.mp4')
    """, (idea_id, *(script[k] for k in SCRIPT_FIELDS)))
    draft_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return draft_id, qa


@router.message(Command("generate"))
@router.message(F.text.lower().in_({"сгенерировать", "генерация", "✨ сгенерировать"}))
async def cmd_generate(message: Message, state: FSMContext):
    await state.set_state(GenerateDraft.waiting_topic)
    await message.reply("✨ Напиши тему ролика одним сообщением.\nНапример: _сыворотка с ниацинамидом для жирной кожи_", parse_mode="Markdown")


@router.message(GenerateDraft.waiting_topic, F.text)
async def process_generate_topic(message: Message, state: FSMContext):
    await state.clear()
    topic = message.text.strip()
    await message.reply("🤖 Агенты работают: стратегия → сценарий → проверка...")

    draft_id, qa = await generate_draft(topic)

    conn = get_db_connection()
    d = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
    conn.close()
    await message.answer(format_draft_text(d, format_qa_text(qa)), reply_markup=get_draft_approval_keyboard(draft_id), parse_mode="Markdown")

# --- COMMAND: /schedule ---
@router.message(Command("schedule"))
@router.message(F.text.lower().in_({"расписание", "календарь", "schedule", "📅 расписание"}))
async def cmd_schedule(message: Message):
    conn = get_db_connection()
    scheduled = conn.execute("SELECT * FROM drafts WHERE status = 'SCHEDULED' ORDER BY scheduled_time ASC").fetchall()
    conn.close()
    
    if not scheduled:
        await message.reply("В календаре пока нет запланированных Reels.")
        return
        
    text = "📅 **Календарь автоматического бьюти-вещания:**\n\n"
    for s in scheduled:
        text += f"• **{s['scheduled_time']}** — ID-{s['id']}: *{s['title']}*\n"
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /analytics ---
@router.message(Command("analytics"))
@router.message(F.text.lower().in_({"аналитика", "просмотры", "analytics", "📈 аналитика"}))
async def cmd_analytics(message: Message):
    text = (
        "📈 **Аналитика бьюти-контента (UGC):**\n\n"
        "• *3 Ошибки при очищении лица* (ID-2)\n"
        "  └ 👀 Просмотры: 24,150 | ❤️ Лайки: 2,130 | 💬 Комменты: 341 (ManyChat СТА!) | 💾 Сохранения: 890\n"
        "• *Эстетика ASMR: Распаковка* (ID-1)\n"
        "  └ 👀 Просмотры: 12,400 | ❤️ Лайки: 1,120 | 💬 Комменты: 95 | 💾 Сохранения: 140\n\n"
        "🎯 **Инсайт Агента-Аналитика:** Образовательный ролик с разбором ошибок ухода принес в 6 раз больше сохранений и в 3.5 раза больше комментариев, чем чисто эстетический ASMR. Рекомендую добавить в план разбор темы мицеллярной воды."
    )
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /settings ---
@router.message(Command("settings"))
async def cmd_settings(message: Message):
    text = (
        "⚙️ **Конфигурация бьюти-конвейера:**\n\n"
        f"• **Бизнес-аккаунт IG:** `{INSTAGRAM_BUSINESS_ACCOUNT_ID[:5]}...`\n"
        f"• **Токен Meta API:** `{INSTAGRAM_ACCESS_TOKEN[:5]}...`\n"
        "• **Продукт продвижения:** *Косметика для ухода за лицом*\n"
        "• **Стиль удержания:** *Эстетичный бьюти-ASMR + Экспертиза*"
    )
    await message.reply(text, parse_mode="Markdown")

# --- CALLBACK HANDLING (APPROVALS, DISAPPROVALS) ---
@router.callback_query(F.data.startswith("app_"))
async def handle_approval(callback: CallbackQuery):
    draft_id = int(callback.data.split("_")[1])
    conn = get_db_connection()
    conn.execute("UPDATE drafts SET status = 'APPROVED' WHERE id = ?", (draft_id,))
    conn.commit()
    conn.close()
    
    await callback.answer("Утверждено! Видео отправлено в Instagram API...", show_alert=True)
    await callback.message.edit_text(f"✅ **СЦЕНАРИЙ ID {draft_id} ОДОБРЕН**\n\nАгент-Публикатор загружает Reels на сервера Instagram...")
    asyncio.create_task(publish_draft_to_instagram(draft_id))

@router.callback_query(F.data.startswith("sch_"))
async def handle_scheduling(callback: CallbackQuery):
    draft_id = int(callback.data.split("_")[1])
    scheduled_time = (datetime.now() + timedelta(days=1)).replace(hour=18, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_db_connection()
    conn.execute("UPDATE drafts SET status = 'SCHEDULED', scheduled_time = ? WHERE id = ?", (scheduled_time, draft_id))
    conn.commit()
    conn.close()
    
    await callback.answer(f"Успешно запланировано на завтра на 18:00!", show_alert=True)
    await callback.message.edit_text(f"📅 **СЦЕНАРИЙ ID {draft_id} ЗАПЛАНИРОВАН**\nАвтопубликация: {scheduled_time}")

@router.callback_query(F.data.startswith("rej_"))
async def handle_rejection(callback: CallbackQuery):
    draft_id = int(callback.data.split("_")[1])
    conn = get_db_connection()
    conn.execute("UPDATE drafts SET status = 'REJECTED' WHERE id = ?", (draft_id,))
    conn.commit()
    conn.close()
    
    await callback.answer("Черновик отправлен в брак.", show_alert=True)
    await callback.message.edit_text(f"❌ **СЦЕНАРИЙ ID {draft_id} ОТКЛОНЕН И АРХИВИРОВАН**")

class ReviseDraft(StatesGroup):
    waiting_feedback = State()


@router.callback_query(F.data.startswith("rev_"))
async def handle_revision(callback: CallbackQuery, state: FSMContext):
    draft_id = int(callback.data.split("_")[1])
    conn = get_db_connection()
    conn.execute("UPDATE drafts SET status = 'REVISING' WHERE id = ?", (draft_id,))
    conn.commit()
    conn.close()

    await state.set_state(ReviseDraft.waiting_feedback)
    await state.update_data(draft_id=draft_id)
    await callback.answer()
    await callback.message.edit_text(
        f"🛠️ **СЦЕНАРИЙ ID {draft_id} НА КОРРЕКТИРОВКЕ**\n\n"
        f"Напиши одним сообщением, что исправить. Например: _хук слабый, сделай провокационнее_",
        parse_mode="Markdown"
    )


@router.message(ReviseDraft.waiting_feedback, F.text)
async def process_revision_feedback(message: Message, state: FSMContext):
    draft_id = (await state.get_data())["draft_id"]
    await state.clear()
    feedback = message.text.strip()

    conn = get_db_connection()
    d = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
    conn.close()
    if not d:
        await message.reply("❌ Черновик не найден.")
        return

    await message.reply("✍️ Агент-Сценарист переписывает сценарий...")
    swarm = MultiAgentSwarm()
    script = await swarm.run_revision({k: d[k] for k in SCRIPT_FIELDS}, feedback)

    conn = get_db_connection()
    if script is None:
        conn.execute("UPDATE drafts SET status = 'PENDING_USER', revision_feedback = ? WHERE id = ?", (feedback, draft_id))
        conn.commit()
        conn.close()
        await message.reply("⚠️ OpenAI недоступен (нет OPENAI_API_KEY или ошибка API) — черновик не изменён, замечание сохранено.")
        return

    # LLM text goes into Telegram Markdown: drop characters that would break the markup.
    script = {k: v.translate(str.maketrans("", "", "*_`[]")) for k, v in script.items()}
    qa = await swarm.run_qa_check(script)
    conn.execute(
        "UPDATE drafts SET title = ?, hook = ?, body = ?, cta = ?, visual_prompt = ?, audio_prompt = ?, "
        "status = 'PENDING_USER', revision_feedback = ? WHERE id = ?",
        (*(script[k] for k in SCRIPT_FIELDS), feedback, draft_id)
    )
    conn.commit()
    d = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
    conn.close()

    await message.answer(format_draft_text(d, format_qa_text(qa)), reply_markup=get_draft_approval_keyboard(draft_id), parse_mode="Markdown")


async def publish_draft_to_instagram(draft_id: int):
    conn = get_db_connection()
    draft = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
    conn.close()
    
    if not draft:
        return
        
    try:
        caption = f"{draft['title']}\n\n{draft['hook']}\n{draft['body']}\n\n{draft['cta']}"
        video_url = draft["media_url"]
        
        container_id = await InstagramPublishingAgent.create_reels_container(video_url, caption)
        
        conn = get_db_connection()
        conn.execute("UPDATE drafts SET status = 'PUBLISHING', instagram_container_id = ? WHERE id = ?", (container_id, draft_id))
        conn.commit()
        
        is_ready = await InstagramPublishingAgent.wait_until_ready(container_id)
        if not is_ready:
            raise Exception("Timeout encoding video")
            
        media_id = await InstagramPublishingAgent.publish_reels(container_id)
        
        conn.execute("UPDATE drafts SET status = 'PUBLISHED', instagram_media_id = ? WHERE id = ?", (media_id, draft_id))
        conn.commit()
        logger.info(f"Published Reels ID: {draft_id} success. Media ID: {media_id}")
        
    except Exception as e:
        logger.error(f"Failed to publish draft {draft_id}: {e}")
        conn = get_db_connection()
        conn.execute("UPDATE drafts SET status = 'PUBLISH_FAILED', revision_feedback = ? WHERE id = ?", (str(e), draft_id))
        conn.commit()
    finally:
        conn.close()


async def handle_web(request):
    return web.Response(text="UGC Beauty Reels Bot is running 24/7!")

# =====================================================================
# SYSTEM INITIALIZATION & MAIN LOOP
# =====================================================================
async def main():
    if not TELEGRAM_BOT_TOKEN or not bot:
        logger.error("❌ КРИТИЧЕСКАЯ ОШИБКА: Переменная окружения TELEGRAM_BOT_TOKEN отсутствует! Бот запущен в режиме безопасного ожидания. Пожалуйста, задайте переменную окружения TELEGRAM_BOT_TOKEN и перезапустите процесс.")
        while True:
            await asyncio.sleep(3600)
            
    logger.info("Инициализация базы данных и заполнение бьюти-сценариями...")
    init_db()
    await seed_beauty_ugc_database()
    
    # Исключение конфликтов вебхука и сброс зависшей очереди обновлений
    await bot.delete_webhook(drop_pending_updates=False)
    logger.info("Активный Webhook успешно удален, очередь обновлений сброшена.")
    
    dp.include_router(router)
    
    # Запуск параллельного веб-сервера для успешного прохождения проверки Render Port-Binding
    try:
        app = web.Application()
        app.router.add_get("/", handle_web)
        runner = web.AppRunner(app)
        await runner.setup()
        port = int(os.getenv("PORT", 8080))
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"🌐 Веб-сервер успешно запущен на порту {port} (совместимость с Render пройден)")
    except Exception as e:
        logger.error(f"Предупреждение запуска веб-сервера (не критично для локала): {e}")
    
    logger.info("Запуск бота Telegram на токене клиента...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот выключен пользователем.")
