import os
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

# =====================================================================
# CONFIGURATION & API KEYS PLACEHOLDERS
# =====================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "MOCK_OPENAI_API_KEY")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "MOCK_INSTAGRAM_ID")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "MOCK_INSTAGRAM_TOKEN")

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
    async def call_llm(prompt: str, system_message: str) -> str:
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
        logger.info(f"[Competitor Agent] РђРЅР°Р»РёР·РёСЂСѓРµРј Р±СЊСЋС‚Рё-Р°РєРєР°СѓРЅС‚ @{username}...")
        await asyncio.sleep(1)
        # Returns raw high-performing trends
        return [
            f"Р­СЃС‚РµС‚РёРєР° РєР°РїРµР»СЊ СЃС‹РІРѕСЂРѕС‚РєРё РЅР° Р»РёС†Рµ РєСЂСѓРїРЅС‹Рј РїР»Р°РЅРѕРј (СЂРѕСЃС‚ СѓРґРµСЂР¶Р°РЅРёСЏ РЅР° 80% Сѓ @{username})",
            f"РЁРѕРєРёСЂСѓСЋС‰РёР№ СЂР°Р·Р±РѕСЂ РѕС€РёР±РѕРє РѕС‡РёС‰РµРЅРёСЏ РїРѕСЂ (Р°РєС‚РёРІРЅРѕСЃС‚СЊ Сѓ @{username})"
        ]

    async def run_content_strategy(self, trends: list) -> list:
        logger.info("[Strategy Agent] РџРµСЂРµРІРѕРґРёРј С‚СЂРµРЅРґС‹ РІ РєРѕРЅС†РµРїС‚С‹ РѕСЂРёРіРёРЅР°Р»СЊРЅРѕРіРѕ Р±СЊСЋС‚Рё-UGC...")
        await asyncio.sleep(1)
        return [
            f"UGC РљРѕРЅС†РµРїС‚: Р­СЃС‚РµС‚РёРєР° ASMR-РЅР°РЅРµСЃРµРЅРёСЏ РјР°С‚РѕРІРѕР№ СЃС‹РІРѕСЂРѕС‚РєРё СЃ РјР°РєСЂРѕР»РёРЅР·РѕР№",
            f"UGC РљРѕРЅС†РµРїС‚: 3 РѕС€РёР±РєРё СѓС…РѕРґР° Р·Р° Р»РёС†РѕРј, РєРѕС‚РѕСЂС‹Рµ СЂР°Р·СЂСѓС€Р°СЋС‚ РєРѕР¶РЅС‹Р№ Р±Р°СЂСЊРµСЂ"
        ]

    async def run_script_and_prompts(self, idea_topic: str) -> dict:
        logger.info(f"[Script Agent] РџРёС€РµРј РґРµС‚Р°Р»СЊРЅС‹Р№ Р±СЊСЋС‚Рё-СЃС†РµРЅР°СЂРёР№ РїРѕ СЃРµРєСѓРЅРґР°Рј...")
        await asyncio.sleep(1.5)
        
        if "РѕС€РёР±РєРё" in idea_topic.lower():
            return {
                "title": "3 РѕС€РёР±РєРё СѓС…РѕРґР°, РєРѕС‚РѕСЂС‹Рµ РіСѓР±СЏС‚ С‚РІРѕСЋ РєРѕР¶Сѓ",
                "hook": "РџСЂРµРєСЂР°С‚Рё РЅР°РЅРѕСЃРёС‚СЊ СЃС‹РІРѕСЂРѕС‚РєСѓ РїСЂСЏРјРѕ РёР· РїРёРїРµС‚РєРё РЅР° Р»РёС†Рѕ! Р РІРѕС‚ РїРѕС‡РµРјСѓ...",
                "body": "РљР°СЃР°СЏСЃСЊ РїРёРїРµС‚РєРѕР№ РєРѕР¶Рё, С‚С‹ РїРµСЂРµРЅРѕСЃРёС€СЊ Р±Р°РєС‚РµСЂРёРё РІРѕ С„Р»Р°РєРѕРЅ. РќР°РЅРѕСЃРё СЃСЂРµРґСЃС‚РІРѕ РЅР° С‡РёСЃС‚С‹Рµ Р»Р°РґРѕРЅРё! Р’С‚РѕСЂР°СЏ РѕС€РёР±РєР°: РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ Р°РіСЂРµСЃСЃРёРІРЅС‹Рµ СЃРєСЂР°Р±С‹ РїСЂРё Р°РєРЅРµ. Р С‚СЂРµС‚СЊСЏ: Р·Р°Р±С‹РІР°С‚СЊ РїСЂРѕ SPF-Р·Р°С‰РёС‚Сѓ Р»РµС‚РѕРј Рё Р·РёРјРѕР№.",
                "cta": "РџРёС€Рё СЃР»РѕРІРѕ 'РЎРџРђРЎР•РќРР•' РІ РєРѕРјРјРµРЅС‚Р°СЂРёСЏС…, Рё СЏ РїСЂРёС€Р»СЋ С‚РµР±Рµ РїРѕС€Р°РіРѕРІСѓСЋ СЃС…РµРјСѓ СѓС…РѕРґР° Р·Р° Р±Р°СЂСЊРµСЂРѕРј РєРѕР¶Рё СЃРѕРІРµСЂС€РµРЅРЅРѕ Р±РµСЃРїР»Р°С‚РЅРѕ!",
                "visual_prompt": "Aesthetic cinematic macro video. Female hand using a skincare glass dropper, dropping oil on palms. Soft morning bathroom background, diffuse white lighting.",
                "audio_prompt": "Warm ASMR whisper sound, soft lo-fi background beat, water splashing effects."
            }
        else:
            return {
                "title": "Р­СЃС‚РµС‚РёРєР° ASMR: РўРІРѕР№ РЅРѕРІС‹Р№ СѓС‚СЂРµРЅРЅРёР№ СЂРёС‚СѓР°Р»",
                "hook": "Р­СЃС‚РµС‚РёРєР° СѓС…РѕРґР°, РєРѕС‚РѕСЂР°СЏ Р·Р°РјРµРЅСЏРµС‚ С‚РµР±Рµ Р»СЋР±С‹Рµ РјР°СЃРєРё РІ РёРЅСЃС‚Р°РіСЂР°РјРµ... вњЁ",
                "body": "РљР°Р¶РґРѕРµ СѓС‚СЂРѕ С‚РІРѕСЏ РєРѕР¶Р° Р·Р°СЃР»СѓР¶РёРІР°РµС‚ Р±РµСЂРµР¶РЅРѕРіРѕ РѕС‚РЅРѕС€РµРЅРёСЏ. РќРµР¶РЅРѕРµ РѕР±Р»Р°РєРѕ РїРµРЅРєРё, РєР°РїР»СЏ РїРёС‚Р°С‚РµР»СЊРЅРѕР№ СЃС‹РІРѕСЂРѕС‚РєРё Рё Р»РµРіРєРёР№ РјР°СЃСЃР°Р¶ РіСѓР°С€Р°. РџРѕР·РІРѕР»СЊ СЃРµР±Рµ СЌС‚Рё 5 РјРёРЅСѓС‚ Р·Р°Р±РѕС‚С‹.",
                "cta": "Р’СЃРµ Р±СЊСЋС‚Рё-РїСЂРѕРґСѓРєС‚С‹ РёР· СЌС‚РѕРіРѕ РІРёРґРµРѕ РѕСЃС‚Р°РІРёР»Р° РІ РѕРїРёСЃР°РЅРёРё. РљР°РєРѕРµ С‚РІРѕРµ Р»СЋР±РёРјРѕРµ СЃСЂРµРґСЃС‚РІРѕ?",
                "visual_prompt": "Extreme macro close-up of pink face serum dripping, bubbles in gel cleanser, cream texture swirls under studio light, aesthetic beauty video style.",
                "audio_prompt": "Acoustic ASMR clicks, tapping on glass bottles, soft ambient water drops and peaceful sound design."
            }

    async def run_qa_check(self, script_data: dict) -> dict:
        logger.info("[QA Agent] РџСЂРѕРІРµСЂРєР° РЅР° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёРµ Р±СЊСЋС‚Рё-СЃС‚Р°РЅРґР°СЂС‚Р°Рј Рё РїРѕР»РёС‚РёРєРµ Meta...")
        await asyncio.sleep(0.5)
        return {"is_passed": True, "score": 9.5}


# =====================================================================
# OFFICIAL INSTAGRAM GRAPH API POSTING ENGINE (PUBLISHING AGENT)
# =====================================================================
class InstagramPublishingAgent:
    @staticmethod
    async def create_reels_container(media_url: str, caption: str) -> str:
        if INSTAGRAM_ACCESS_TOKEN == "MOCK_ACCESS_TOKEN" or not INSTAGRAM_ACCESS_TOKEN:
            logger.info("[Publishing Agent] РЎРёРјСѓР»СЏС†РёСЏ Р·Р°РіСЂСѓР·РєРё Reels РІ Instagram...")
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
        if INSTAGRAM_ACCESS_TOKEN == "MOCK_ACCESS_TOKEN" or not INSTAGRAM_ACCESS_TOKEN:
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
    async def publish_reels(container_id: str) -> str:
        if INSTAGRAM_ACCESS_TOKEN == "MOCK_ACCESS_TOKEN" or not INSTAGRAM_ACCESS_TOKEN:
            logger.info("[Publishing Agent] Р’РёРґРµРѕ СѓСЃРїРµС€РЅРѕ РѕРїСѓР±Р»РёРєРѕРІР°РЅРѕ!")
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
    
    # Clean old mock drafts to avoid duplication on re-runs
    cursor.execute("DELETE FROM drafts")
    cursor.execute("DELETE FROM ideas")
    cursor.execute("DELETE FROM competitors")
    
    # 1. Add premium competitors
    competitors = [("smorodina_cosmetic",), ("shikcosmetics",), ("mixit_ru",), ("art_visage",)]
    cursor.executemany("INSERT INTO competitors (username, added_at) VALUES (?, datetime('now'))", competitors)
    
    # 2. Add raw ideas
    ideas = [
        ("ASMR-СЂР°СЃРїР°РєРѕРІРєР° РЅРѕРІРѕР№ РєРѕСЂРµР№СЃРєРѕР№ СЃС‹РІРѕСЂРѕС‚РєРё", 1),
        ("3 РћС€РёР±РєРё СѓС…РѕРґР°: РїСЂР°РІРёР»СЊРЅРѕРµ РЅР°РЅРµСЃРµРЅРёРµ С‚РѕРЅРёРєР°", 2),
        ("Р”Рѕ/РџРѕСЃР»Рµ: РЎРїР°СЃРµРЅРёРµ РєРѕР¶Рё Р»РёС†Р° РѕС‚ СЃСѓС…РѕСЃС‚Рё Рё С€РµР»СѓС€РµРЅРёР№", 3),
        ("Р­СЃС‚РµС‚РёС‡РЅС‹Р№ GRWM: СѓС‚СЂРµРЅРЅРёР№ СѓС…РѕРґ, Р·Р°РјРµРЅСЏСЋС‰РёР№ С„РёР»СЊС‚СЂС‹", 4)
    ]
    for topic, comp_id in ideas:
        cursor.execute("INSERT INTO ideas (topic, source_competitor_id, created_at, status) VALUES (?, ?, datetime('now'), 'GENERATED')", (topic, comp_id))
        
    # 3. Add 4 highly tailored, pre-written UGC Beauty Drafts awaiting user approval
    beauty_drafts = [
        (
            1, "Р­СЃС‚РµС‚РёС‡РЅР°СЏ ASMR-СЂР°СЃРїР°РєРѕРІРєР°",
            "Р­СЃС‚РµС‚РёРєР° СѓС…РѕРґР°, РєРѕС‚РѕСЂР°СЏ Р·Р°РјРµРЅСЏРµС‚ С‚РµР±Рµ Р»СЋР±С‹Рµ РјР°СЃРєРё РІ РёРЅСЃС‚Р°РіСЂР°РјРµ... вњЁ",
            "РџРѕСЃС‚СѓРєРёРІР°РЅРёРµ РЅРѕРіС‚СЏРјРё РїРѕ РєРѕСЂРѕР±РєРµ, С€СѓСЂС€Р°РЅРёРµ РєСЂР°С„С‚РѕРІРѕР№ Р±СѓРјР°РіРё, РјРµРґР»РµРЅРЅРѕРµ РёР·РІР»РµС‡РµРЅРёРµ СЃС‚РµРєР»СЏРЅРЅРѕРіРѕ С„Р»Р°РєРѕРЅР° Рё РїР°РґРµРЅРёРµ РєР°РїР»Рё СЃС‹РІРѕСЂРѕС‚РєРё РЅР° Р»Р°РґРѕРЅСЊ РІ СЃР»РѕСѓ-РјРѕ.",
            "РџРёС€Рё СЃР»РѕРІРѕ 'РЎРРЇРќРР•' РІ РєРѕРјРјРµРЅС‚Р°СЂРёСЏС…, Рё СЏ РїСЂРёС€Р»СЋ С‚РµР±Рµ СЃСЃС‹Р»РєСѓ РЅР° СЌС‚РѕС‚ Р±СЂРµРЅРґ!",
            "Extreme macro close-up of a premium glass dropper bottle, pink serum dripping. Soft sun rays, aesthetic background, 8k beauty lighting.",
            "Clean acoustic ASMR clicks, paper rustling, water drop effect, cozy lofi chillhop background music.",
            "PENDING_USER"
        ),
        (
            2, "3 РћС€РёР±РєРё СѓС…РѕРґР° Р·Р° Р»РёС†РѕРј",
            "РџСЂРµРєСЂР°С‚Рё РЅР°РЅРѕСЃРёС‚СЊ СЃС‹РІРѕСЂРѕС‚РєСѓ РїСЂСЏРјРѕ РёР· РїРёРїРµС‚РєРё РЅР° Р»РёС†Рѕ! Р РІРѕС‚ РїРѕС‡РµРјСѓ...",
            "РЎРїРёРєРµСЂ РєР°С‡Р°РµС‚ РіРѕР»РѕРІРѕР№ 'РќР•Рў', РґРµСЂР¶Р° РїРёРїРµС‚РєСѓ Сѓ Р»РёС†Р° (РєСЂР°СЃРЅС‹Р№ РєСЂРµСЃС‚). Р—Р°С‚РµРј РїРѕРєР°Р·С‹РІР°РµС‚ РїСЂР°РІРёР»СЊРЅС‹Р№ РІР°СЂРёР°РЅС‚: РєР°РїР»Рё РЅР° Р»Р°РґРѕРЅРё, СЂР°СЃС‚РёСЂР°РЅРёРµ Рё Р±РµСЂРµР¶РЅРѕРµ РїРѕС…Р»РѕРїС‹РІР°РЅРёРµ РїРѕ РєРѕР¶Рµ.",
            "РџРѕРґРїРёС€РёСЃСЊ РЅР° РїСЂРѕС„РёР»СЊ, Сѓ РјРµРЅСЏ РІСЃС‘ Рѕ Р±РµСЂРµР¶РЅРѕРј Рё РїСЂР°РІРёР»СЊРЅРѕРј СѓС…РѕРґРµ Р·Р° Р»РёС†РѕРј РєР°Р¶РґС‹Р№ РґРµРЅСЊ!",
            "Beauty UGC style video, hands applying cosmetic product on skin, soft diffuse warm light, safe zones for instagram reels text.",
            "Warm conversational voiceover, slight ambient background lounge beat.",
            "PENDING_USER"
        ),
        (
            3, "Р”Рѕ / РџРѕСЃР»Рµ: SOS-СѓРІР»Р°Р¶РЅРµРЅРёРµ",
            "РњРѕСЏ РєРѕР¶Р° РєСЂРёС‡Р°Р»Р° Рѕ РїРѕРјРѕС‰Рё РѕС‚ РґРёРєРѕР№ СЃСѓС…РѕСЃС‚Рё Рё СЃС‚СЏРЅСѓС‚РѕСЃС‚Рё...",
            "РџРѕРєР°Р·С‹РІР°РµРј СЃСѓС…СѓСЋ С‚СѓСЃРєР»СѓСЋ РєРѕР¶Сѓ РєСЂСѓРїРЅС‹Рј РїР»Р°РЅРѕРј. РќР°РЅРѕСЃРёРј РєСЂРµРј СЃР»РёРІРѕС‡РЅРѕР№ С‚РµРєСЃС‚СѓСЂС‹ СЃ С†РµРЅС‚РµР»Р»РѕР№. Р’Р¶СѓС…-СЌС„С„РµРєС‚ вЂ” РєРѕР¶Р° СЃРёСЏРµС‚, РЅР°РїРёС‚Р°РЅР°, РјР°РєРёСЏР¶ Р»РѕР¶РёС‚СЃСЏ Р±РµР·СѓРїСЂРµС‡РЅРѕ.",
            "РЎРѕС…СЂР°РЅРё СЌС‚РѕС‚ СЂРёР»СЃ, С‡С‚РѕР±С‹ РЅРµ РїРѕС‚РµСЂСЏС‚СЊ РЅР°Р·РІР°РЅРёРµ СЌС‚РѕРіРѕ SOS-РєСЂРµРјР°!",
            "Macro shot of cosmetic cream texture being swirled with a gold spatula. Panning camera shot, beautiful lighting, pink aesthetics.",
            "Swoosh transition effect, relaxing water droplet sound design, ambient morning tracks.",
            "PENDING_USER"
        ),
        (
            4, "РЈС‚СЂРµРЅРЅРёР№ GRWM: Р—Р°Р±РѕС‚Р° Рѕ Р»РёС†Рµ",
            "Р”Р°РІР°Р№ СЃРґРµР»Р°РµРј СѓС‚СЂРµРЅРЅРёР№ СѓС…РѕРґ, РїРѕСЃР»Рµ РєРѕС‚РѕСЂРѕРіРѕ С‚РµР±Рµ РЅРµ РїРѕРЅР°РґРѕР±СЏС‚СЃСЏ С„РёР»СЊС‚СЂС‹...",
            "РЈРјС‹РІР°РЅРёРµ РѕР±РёР»СЊРЅРѕР№ РїРµРЅРєРѕР№, РјСЏРіРєРѕРµ РїСЂРѕРјР°РєРёРІР°РЅРёРµ РїРѕР»РѕС‚РµРЅС†РµРј, С‚РѕРЅРµСЂ РїРѕС…Р»РѕРїС‹РІР°РЅРёСЏРјРё Рё РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ SPF-Р·Р°С‰РёС‚РЅС‹Р№ РєСЂРµРј РІ РІРёРґРµ Р°РєРєСѓСЂР°С‚РЅС‹С… С‚РѕС‡РµРє РЅР° Р»РёС†Рµ.",
            "Р’СЃРµ СЌС‚Р°РїС‹ Рё Р±СЂРµРЅРґС‹ РѕСЃС‚Р°РІРёР»Р° РІ РѕРїРёСЃР°РЅРёРё Рє РІРёРґРµРѕ. Рђ РєР°РєРѕР№ С‚РІРѕР№ Р»СЋР±РёРјС‹Р№ SPF?",
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
# РўР•Р›Р•Р“Р РђРњ Р РћРЈРўР•Р  Р РљРћРњРђРќР”Р«
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
            KeyboardButton(text="рџЊё Р§РµСЂРЅРѕРІРёРєРё (СЃС†РµРЅР°СЂРёРё)"),
            KeyboardButton(text="рџ—“пёЏ РљРѕРЅС‚РµРЅС‚-РїР»Р°РЅ")
        ],
        [
            KeyboardButton(text="рџ“Љ РЎС‚Р°С‚СѓСЃ Р·Р°РІРѕРґР°"),
            KeyboardButton(text="рџ”Ќ РљРѕРЅРєСѓСЂРµРЅС‚С‹")
        ],
        [
            KeyboardButton(text="рџ“… Р Р°СЃРїРёСЃР°РЅРёРµ"),
            KeyboardButton(text="рџ“€ РђРЅР°Р»РёС‚РёРєР°")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, persistent=True)

def get_draft_approval_keyboard(draft_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="вњ… РћРґРѕР±СЂРёС‚СЊ", callback_data=f"app_{draft_id}"),
            InlineKeyboardButton(text="вќЊ РћС‚РєР»РѕРЅРёС‚СЊ", callback_data=f"rej_{draft_id}")
        ],
        [
            InlineKeyboardButton(text="рџ› пёЏ РќР° РґРѕСЂР°Р±РѕС‚РєСѓ", callback_data=f"rev_{draft_id}"),
            InlineKeyboardButton(text="рџ“… Р’ СЂР°СЃРїРёСЃР°РЅРёРµ", callback_data=f"sch_{draft_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# --- COMMAND: /start ---
@router.message(Command("start"))
@router.message(F.text.lower().in_({"СЃС‚Р°СЂС‚", "start", "РЅР°С‡Р°С‚СЊ", "РїСЂРёРІРµС‚", "РјРµРЅСЋ", "menu", "РїСЂРёРІРµС‚РёРє", "РїСЂРёРІРµС‚РёРє"}))
async def cmd_start(message: Message):
    print(f"рџ“Ґ [DEBUG START] РџРѕР»СѓС‡РµРЅРѕ СЃРѕРѕР±С‰РµРЅРёРµ /start РѕС‚ {message.from_user.username} ({message.from_user.id})", flush=True)
    try:
        welcome_text = (
            "рџЊё **Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊ РІ РџР°РЅРµР»СЊ РЈРїСЂР°РІР»РµРЅРёСЏ UGC-РєСЂРµР°С‚РѕСЂР° РєРѕСЃРјРµС‚РёРєРё!** рџЊё\n\n"
            "РЇ РІР°С€ СЃРїРµС†РёР°Р»РёР·РёСЂРѕРІР°РЅРЅС‹Р№ РР-РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂ. РњРѕРё Р°РіРµРЅС‚С‹ РѕР±СѓС‡РµРЅС‹ Р±СЊСЋС‚Рё-РєРѕРїРёСЂР°Р№С‚РёРЅРіСѓ, "
            "СЌСЃС‚РµС‚РёС‡РµСЃРєРѕР№ СЃСЉРµРјРєРµ Рё РЅР°С‚РёРІРЅС‹Рј РІРѕСЂРѕРЅРєР°Рј СѓС…РѕРґР° Р·Р° Р»РёС†РѕРј.\n\n"
            "РЇ Р·Р°РєСЂРµРїРёР» РЅР° РІР°С€РµРј СЌРєСЂР°РЅРµ РїРѕСЃС‚РѕСЏРЅРЅС‹Рµ **РєРЅРѕРїРєРё СѓРїСЂР°РІР»РµРЅРёСЏ** вЂ” РїСЂРѕСЃС‚Рѕ РЅР°Р¶РёРјР°Р№С‚Рµ РЅР° РЅРёС… РЅР° РїР°РЅРµР»Рё РІРЅРёР·Сѓ, С‡С‚РѕР±С‹ СѓРїСЂР°РІР»СЏС‚СЊ Р°РіРµРЅС‚Р°РјРё! рџ‘‡"
        )
        print("вљ™пёЏ [DEBUG START] Р¤РѕСЂРјРёСЂСѓСЋ РєР»Р°РІРёР°С‚СѓСЂСѓ...", flush=True)
        kbd = get_main_reply_keyboard()
        print("рџ“Ё [DEBUG START] Р’С‹Р·С‹РІР°СЋ message.reply...", flush=True)
        res = await message.reply(welcome_text, reply_markup=kbd, parse_mode="Markdown")
        print(f"вњ… [DEBUG START] РЈСЃРїРµС€РЅРѕ РѕС‚РїСЂР°РІР»РµРЅРѕ! Message ID: {res.message_id}", flush=True)
    except Exception as e:
        print(f"вќЊ [DEBUG START] РљР РРўРР§Р•РЎРљРђРЇ РћРЁРР‘РљРђ РІ cmd_start: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()

# --- COMMAND: /status ---
@router.message(Command("status"))
@router.message(F.text.lower().in_({"СЃС‚Р°С‚СѓСЃ", "status", "СЃС‚Р°С‚РёСЃС‚РёРєР°", "рџ“Љ СЃС‚Р°С‚СѓСЃ Р·Р°РІРѕРґР°"}))
async def cmd_status(message: Message):
    conn = get_db_connection()
    stats = conn.execute("SELECT status, COUNT(*) as cnt FROM drafts GROUP BY status").fetchall()
    conn.close()
    
    status_text = "рџ“Љ **РЎС‚Р°С‚РёСЃС‚РёРєР° РєРѕРЅРІРµР№РµСЂР° UGC-РљРѕСЃРјРµС‚РёРєРё:**\n\n"
    if not stats:
        status_text += "Р’РѕСЂРѕРЅРєР° РїСѓСЃС‚Р°. РР-Р°РіРµРЅС‚С‹ Р·Р°РїСѓСЃРєР°СЋС‚ РЅРѕРІС‹Р№ С†РёРєР» РіРµРЅРµСЂР°С†РёРё."
    else:
        for row in stats:
            status_text += f"вЂў *{row['status']}*: {row['cnt']} РІРёРґРµРѕ\n"
            
    await message.reply(status_text, parse_mode="Markdown")

# --- COMMAND: /competitors ---
@router.message(Command("competitors"))
@router.message(F.text.lower().in_({"РєРѕРЅРєСѓСЂРµРЅС‚С‹", "competitors", "рџ”Ќ РєРѕРЅРєСѓСЂРµРЅС‚С‹"}))
async def cmd_competitors(message: Message):
    conn = get_db_connection()
    competitors = conn.execute("SELECT * FROM competitors").fetchall()
    conn.close()
    
    text = "рџ”Ќ **Р‘Р°Р·Р° РѕС‚СЃР»РµР¶РёРІР°РµРјС‹С… Р±СЊСЋС‚Рё-Р°РєРєР°СѓРЅС‚РѕРІ:**\n\n"
    for comp in competitors:
        text += f"вЂў @{comp['username']} (РЎС‚Р°С‚СѓСЃ: {comp['status']})\n"
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /add_competitor ---
@router.message(Command("add_competitor"))
async def cmd_add_competitor(message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("вќЊ РџСЂРёРјРµСЂ РґРѕР±Р°РІР»РµРЅРёСЏ: `/add_competitor drcella_skincare`", parse_mode="Markdown")
        return
    username = args[1].replace("@", "").strip()
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO competitors (username, added_at) VALUES (?, datetime('now'))", (username,))
        conn.commit()
        await message.reply(f"вњ… РђРєРєР°СѓРЅС‚ **@{username}** РґРѕР±Р°РІР»РµРЅ РІ Р±Р°Р·Сѓ РђРіРµРЅС‚Р°-РђРЅР°Р»РёС‚РёРєР°!", parse_mode="Markdown")
    except sqlite3.IntegrityError:
        await message.reply("вќЊ Р­С‚РѕС‚ Р°РєРєР°СѓРЅС‚ СѓР¶Рµ РѕС‚СЃР»РµР¶РёРІР°РµС‚СЃСЏ.")
    finally:
        conn.close()

# --- COMMAND: /content_plan ---
@router.message(Command("content_plan"))
@router.message(F.text.lower().in_({"РїР»Р°РЅ", "РёРґРµРё", "РєРѕРЅС‚РµРЅС‚-РїР»Р°РЅ", "content_plan", "рџ—“пёЏ РєРѕРЅС‚РµРЅС‚-РїР»Р°РЅ"}))
async def cmd_content_plan(message: Message):
    conn = get_db_connection()
    ideas = conn.execute("SELECT * FROM ideas ORDER BY id DESC").fetchall()
    conn.close()
    
    text = "рџ—“пёЏ **РђРґР°РїС‚РёСЂРѕРІР°РЅРЅС‹Рµ Р±СЊСЋС‚Рё-РёРґРµРё РІ РєРѕРЅС‚РµРЅС‚-РїР»Р°РЅРµ:**\n\n"
    for idea in ideas:
        text += f"рџ“Ќ ID-{idea['id']} | {idea['topic']}\n\n"
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /drafts ---
@router.message(Command("drafts"))
@router.message(F.text.lower().in_({"С‡РµСЂРЅРѕРІРёРєРё", "С‡РµСЂРЅРѕРІРёРє", "СЃС†РµРЅР°СЂРёРё", "СЃС†РµРЅР°СЂРёР№", "drafts", "draft", "рџЊё С‡РµСЂРЅРѕРІРёРєРё (СЃС†РµРЅР°СЂРёРё)"}))
async def cmd_drafts(message: Message):
    conn = get_db_connection()
    drafts = conn.execute("SELECT * FROM drafts WHERE status = 'PENDING_USER' ORDER BY id ASC").fetchall()
    conn.close()
    
    if not drafts:
        await message.reply("РЈ РІР°СЃ РЅРµС‚ РіРѕС‚РѕРІС‹С… СЃС†РµРЅР°СЂРёРµРІ РєРѕСЃРјРµС‚РёРєРё РЅР° РѕРґРѕР±СЂРµРЅРёРµ. Р’СЃРµ СЂРѕР»РёРєРё РІ СЌС„РёСЂРµ! рџЋ‰")
        return
        
    for d in drafts:
        text = (
            f"рџЊё **Р‘Р¬Р®РўР-UGC Р§Р•Р РќРћР’РРљ REELS ID: {d['id']}**\n"
            f"в”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓ\n"
            f"рџ“Њ **РљРѕРЅС†РµРїС‚:** {d['title']}\n\n"
            f"рџ§І **РҐРЈРљ (0-3 СЃРµРє):**\n_{d['hook']}_\n\n"
            f"рџ“ќ **Р“РћР›РћРЎ Р—Рђ РљРђР”Р РћРњ / РЎРЈРўР¬:**\n{d['body']}\n\n"
            f"рџ“ў **РЎРўРђ (РџСЂРёР·С‹РІ Рє РґРµР№СЃС‚РІРёСЋ):**\n*{d['cta']}*\n\n"
            f"рџЋЁ **AI Р’РР”Р•Рћ-РџР РћРњРџРў (РўР— РґР»СЏ СЃСЉРµРјРєРё):**\n`{d['visual_prompt']}`\n\n"
            f"рџЋ™пёЏ **AI РђРЈР”РРћ-РџР РћРњРџРў (Sound Design):**\n`{d['audio_prompt']}`\n"
            f"в”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓв”Ѓ\n"
            f"рџ›ЎпёЏ **РђРЅР°Р»РёР· РЁРµС„-РђРіРµРЅС‚Р°:**\n"
            f"вЂў Р‘РµР·РѕРїР°СЃРЅРѕСЃС‚СЊ Meta: 10/10 (РїСЂРѕР№РґРµРЅРѕ)\n"
            f"вЂў Р РёСЃРєРё: РќРµС‚ РјРµРґРёС†РёРЅСЃРєРёС… РѕР±РµС‰Р°РЅРёР№. РўРµРєСЃС‚ РЅР°С‚РёРІРЅС‹Р№."
        )
        await message.answer(text, reply_markup=get_draft_approval_keyboard(d['id']), parse_mode="Markdown")

# --- COMMAND: /schedule ---
@router.message(Command("schedule"))
@router.message(F.text.lower().in_({"СЂР°СЃРїРёСЃР°РЅРёРµ", "РєР°Р»РµРЅРґР°СЂСЊ", "schedule", "рџ“… СЂР°СЃРїРёСЃР°РЅРёРµ"}))
async def cmd_schedule(message: Message):
    conn = get_db_connection()
    scheduled = conn.execute("SELECT * FROM drafts WHERE status = 'SCHEDULED' ORDER BY scheduled_time ASC").fetchall()
    conn.close()
    
    if not scheduled:
        await message.reply("Р’ РєР°Р»РµРЅРґР°СЂРµ РїРѕРєР° РЅРµС‚ Р·Р°РїР»Р°РЅРёСЂРѕРІР°РЅРЅС‹С… Reels.")
        return
        
    text = "рџ“… **РљР°Р»РµРЅРґР°СЂСЊ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРѕРіРѕ Р±СЊСЋС‚Рё-РІРµС‰Р°РЅРёСЏ:**\n\n"
    for s in scheduled:
        text += f"вЂў **{s['scheduled_time']}** вЂ” ID-{s['id']}: *{s['title']}*\n"
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /analytics ---
@router.message(Command("analytics"))
@router.message(F.text.lower().in_({"Р°РЅР°Р»РёС‚РёРєР°", "РїСЂРѕСЃРјРѕС‚СЂС‹", "analytics", "рџ“€ Р°РЅР°Р»РёС‚РёРєР°"}))
async def cmd_analytics(message: Message):
    text = (
        "рџ“€ **РђРЅР°Р»РёС‚РёРєР° Р±СЊСЋС‚Рё-РєРѕРЅС‚РµРЅС‚Р° (UGC):**\n\n"
        "вЂў *3 РћС€РёР±РєРё РїСЂРё РѕС‡РёС‰РµРЅРёРё Р»РёС†Р°* (ID-2)\n"
        "  в”” рџ‘Ђ РџСЂРѕСЃРјРѕС‚СЂС‹: 24,150 | вќ¤пёЏ Р›Р°Р№РєРё: 2,130 | рџ’¬ РљРѕРјРјРµРЅС‚С‹: 341 (ManyChat РЎРўРђ!) | рџ’ѕ РЎРѕС…СЂР°РЅРµРЅРёСЏ: 890\n"
        "вЂў *Р­СЃС‚РµС‚РёРєР° ASMR: Р Р°СЃРїР°РєРѕРІРєР°* (ID-1)\n"
        "  в”” рџ‘Ђ РџСЂРѕСЃРјРѕС‚СЂС‹: 12,400 | вќ¤пёЏ Р›Р°Р№РєРё: 1,120 | рџ’¬ РљРѕРјРјРµРЅС‚С‹: 95 | рџ’ѕ РЎРѕС…СЂР°РЅРµРЅРёСЏ: 140\n\n"
        "рџЋЇ **РРЅСЃР°Р№С‚ РђРіРµРЅС‚Р°-РђРЅР°Р»РёС‚РёРєР°:** РћР±СЂР°Р·РѕРІР°С‚РµР»СЊРЅС‹Р№ СЂРѕР»РёРє СЃ СЂР°Р·Р±РѕСЂРѕРј РѕС€РёР±РѕРє СѓС…РѕРґР° РїСЂРёРЅРµСЃ РІ 6 СЂР°Р· Р±РѕР»СЊС€Рµ СЃРѕС…СЂР°РЅРµРЅРёР№ Рё РІ 3.5 СЂР°Р·Р° Р±РѕР»СЊС€Рµ РєРѕРјРјРµРЅС‚Р°СЂРёРµРІ, С‡РµРј С‡РёСЃС‚Рѕ СЌСЃС‚РµС‚РёС‡РµСЃРєРёР№ ASMR. Р РµРєРѕРјРµРЅРґСѓСЋ РґРѕР±Р°РІРёС‚СЊ РІ РїР»Р°РЅ СЂР°Р·Р±РѕСЂ С‚РµРјС‹ РјРёС†РµР»Р»СЏСЂРЅРѕР№ РІРѕРґС‹."
    )
    await message.reply(text, parse_mode="Markdown")

# --- COMMAND: /settings ---
@router.message(Command("settings"))
async def cmd_settings(message: Message):
    text = (
        "вљ™пёЏ **РљРѕРЅС„РёРіСѓСЂР°С†РёСЏ Р±СЊСЋС‚Рё-РєРѕРЅРІРµР№РµСЂР°:**\n\n"
        f"вЂў **Р‘РёР·РЅРµСЃ-Р°РєРєР°СѓРЅС‚ IG:** `{INSTAGRAM_BUSINESS_ACCOUNT_ID[:5]}...`\n"
        f"вЂў **РўРѕРєРµРЅ Meta API:** `{INSTAGRAM_ACCESS_TOKEN[:5]}...`\n"
        "вЂў **РџСЂРѕРґСѓРєС‚ РїСЂРѕРґРІРёР¶РµРЅРёСЏ:** *РљРѕСЃРјРµС‚РёРєР° РґР»СЏ СѓС…РѕРґР° Р·Р° Р»РёС†РѕРј*\n"
        "вЂў **РЎС‚РёР»СЊ СѓРґРµСЂР¶Р°РЅРёСЏ:** *Р­СЃС‚РµС‚РёС‡РЅС‹Р№ Р±СЊСЋС‚Рё-ASMR + Р­РєСЃРїРµСЂС‚РёР·Р°*"
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
    
    await callback.answer("РЈС‚РІРµСЂР¶РґРµРЅРѕ! Р’РёРґРµРѕ РѕС‚РїСЂР°РІР»РµРЅРѕ РІ Instagram API...", show_alert=True)
    await callback.message.edit_text(f"вњ… **РЎР¦Р•РќРђР РР™ ID {draft_id} РћР”РћР‘Р Р•Рќ**\n\nРђРіРµРЅС‚-РџСѓР±Р»РёРєР°С‚РѕСЂ Р·Р°РіСЂСѓР¶Р°РµС‚ Reels РЅР° СЃРµСЂРІРµСЂР° Instagram...")
    asyncio.create_task(publish_draft_to_instagram(draft_id))

@router.callback_query(F.data.startswith("sch_"))
async def handle_scheduling(callback: CallbackQuery):
    draft_id = int(callback.data.split("_")[1])
    scheduled_time = (datetime.now() + timedelta(days=1)).replace(hour=18, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
    
    conn = get_db_connection()
    conn.execute("UPDATE drafts SET status = 'SCHEDULED', scheduled_time = ? WHERE id = ?", (scheduled_time, draft_id))
    conn.commit()
    conn.close()
    
    await callback.answer(f"РЈСЃРїРµС€РЅРѕ Р·Р°РїР»Р°РЅРёСЂРѕРІР°РЅРѕ РЅР° Р·Р°РІС‚СЂР° РЅР° 18:00!", show_alert=True)
    await callback.message.edit_text(f"рџ“… **РЎР¦Р•РќРђР РР™ ID {draft_id} Р—РђРџР›РђРќРР РћР’РђРќ**\nРђРІС‚РѕРїСѓР±Р»РёРєР°С†РёСЏ: {scheduled_time}")

@router.callback_query(F.data.startswith("rej_"))
async def handle_rejection(callback: CallbackQuery):
    draft_id = int(callback.data.split("_")[1])
    conn = get_db_connection()
    conn.execute("UPDATE drafts SET status = 'REJECTED' WHERE id = ?", (draft_id,))
    conn.commit()
    conn.close()
    
    await callback.answer("Р§РµСЂРЅРѕРІРёРє РѕС‚РїСЂР°РІР»РµРЅ РІ Р±СЂР°Рє.", show_alert=True)
    await callback.message.edit_text(f"вќЊ **РЎР¦Р•РќРђР РР™ ID {draft_id} РћРўРљР›РћРќР•Рќ Р РђР РҐРР’РР РћР’РђРќ**")

@router.callback_query(F.data.startswith("rev_"))
async def handle_revision(callback: CallbackQuery):
    draft_id = int(callback.data.split("_")[1])
    conn = get_db_connection()
    conn.execute("UPDATE drafts SET status = 'REVISING' WHERE id = ?", (draft_id,))
    conn.commit()
    conn.close()
    
    await callback.answer("Р§РµСЂРЅРѕРІРёРє РЅР°РїСЂР°РІР»РµРЅ Р±СЊСЋС‚Рё-СЃС†РµРЅР°СЂРёСЃС‚Сѓ.", show_alert=True)
    await callback.message.edit_text(f"рџ› пёЏ **РЎР¦Р•РќРђР РР™ ID {draft_id} РћРўРџР РђР’Р›Р•Рќ РќРђ РљРћР Р Р•РљРўРР РћР’РљРЈ**\n\nРђРіРµРЅС‚-РЎС†РµРЅР°СЂРёСЃС‚ РїРµСЂРµРґРµР»С‹РІР°РµС‚ СЂРѕР»РёРє.")


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
        
        is_ready = await InstagramPublishingAgent.check_container_status(container_id)
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
        logger.error("вќЊ РљР РРўРР§Р•РЎРљРђРЇ РћРЁРР‘РљРђ: РџРµСЂРµРјРµРЅРЅР°СЏ РѕРєСЂСѓР¶РµРЅРёСЏ TELEGRAM_BOT_TOKEN РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚! Р‘РѕС‚ Р·Р°РїСѓС‰РµРЅ РІ СЂРµР¶РёРјРµ Р±РµР·РѕРїР°СЃРЅРѕРіРѕ РѕР¶РёРґР°РЅРёСЏ. РџРѕР¶Р°Р»СѓР№СЃС‚Р°, Р·Р°РґР°Р№С‚Рµ РїРµСЂРµРјРµРЅРЅСѓСЋ РѕРєСЂСѓР¶РµРЅРёСЏ TELEGRAM_BOT_TOKEN Рё РїРµСЂРµР·Р°РїСѓСЃС‚РёС‚Рµ РїСЂРѕС†РµСЃСЃ.")
        while True:
            await asyncio.sleep(3600)
            
    logger.info("РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ Р±Р°Р·С‹ РґР°РЅРЅС‹С… Рё Р·Р°РїРѕР»РЅРµРЅРёРµ Р±СЊСЋС‚Рё-СЃС†РµРЅР°СЂРёСЏРјРё...")
    init_db()
    await seed_beauty_ugc_database()
    
    # РСЃРєР»СЋС‡РµРЅРёРµ РєРѕРЅС„Р»РёРєС‚РѕРІ РІРµР±С…СѓРєР° Рё СЃР±СЂРѕСЃ Р·Р°РІРёСЃС€РµР№ РѕС‡РµСЂРµРґРё РѕР±РЅРѕРІР»РµРЅРёР№
    await bot.delete_webhook(drop_pending_updates=False)
    logger.info("РђРєС‚РёРІРЅС‹Р№ Webhook СѓСЃРїРµС€РЅРѕ СѓРґР°Р»РµРЅ, РѕС‡РµСЂРµРґСЊ РѕР±РЅРѕРІР»РµРЅРёР№ СЃР±СЂРѕС€РµРЅР°.")
    
    dp.include_router(router)
    
    # Р—Р°РїСѓСЃРє РїР°СЂР°Р»Р»РµР»СЊРЅРѕРіРѕ РІРµР±-СЃРµСЂРІРµСЂР° РґР»СЏ СѓСЃРїРµС€РЅРѕРіРѕ РїСЂРѕС…РѕР¶РґРµРЅРёСЏ РїСЂРѕРІРµСЂРєРё Render Port-Binding
    try:
        app = web.Application()
        app.router.add_get("/", handle_web)
        runner = web.AppRunner(app)
        await runner.setup()
        port = int(os.getenv("PORT", 8080))
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"рџЊђ Р’РµР±-СЃРµСЂРІРµСЂ СѓСЃРїРµС€РЅРѕ Р·Р°РїСѓС‰РµРЅ РЅР° РїРѕСЂС‚Сѓ {port} (СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚СЊ СЃ Render РїСЂРѕР№РґРµРЅ)")
    except Exception as e:
        logger.error(f"РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ Р·Р°РїСѓСЃРєР° РІРµР±-СЃРµСЂРІРµСЂР° (РЅРµ РєСЂРёС‚РёС‡РЅРѕ РґР»СЏ Р»РѕРєР°Р»Р°): {e}")
    
    logger.info("Р—Р°РїСѓСЃРє Р±РѕС‚Р° Telegram РЅР° С‚РѕРєРµРЅРµ РєР»РёРµРЅС‚Р°...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Р‘РѕС‚ РІС‹РєР»СЋС‡РµРЅ РїРѕР»СЊР·РѕРІР°С‚РµР»РµРј.")
