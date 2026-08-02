"""
BOT_V3 Database Manager
Version: 3.0
"""

from pathlib import Path
import hashlib
import orjson

from logger import info, error

# ==========================================
# DIRECTORIES
# ==========================================

DATA_DIR = Path("data")
CACHE_DIR = Path("cache")

DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

NEWS_DB = DATA_DIR / "news.json"
CONTENT_DB = DATA_DIR / "content.json"
REDEEM_DB = DATA_DIR / "redeem_codes.json"
CACHE_DB = CACHE_DIR / "cache.json"

# ==========================================
# CREATE DATABASE FILES
# ==========================================

DATABASES = [
    NEWS_DB,
    CONTENT_DB,
    REDEEM_DB,
    CACHE_DB
]

for db in DATABASES:
    if not db.exists():
        db.write_bytes(orjson.dumps([]))

# ==========================================
# JSON FUNCTIONS
# ==========================================

def load_json(file_path):

    try:
        return orjson.loads(file_path.read_bytes())

    except Exception as e:
        error(f"Load JSON Error: {e}")
        return []


def save_json(file_path, data):

    try:
        file_path.write_bytes(
            orjson.dumps(
                data,
                option=orjson.OPT_INDENT_2
            )
        )

    except Exception as e:
        error(f"Save JSON Error: {e}")

# ==========================================
# HASH
# ==========================================

def create_hash(text):

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

# ==========================================
# NEWS
# ==========================================

def news_exists(news_hash):

    database = load_json(NEWS_DB)

    return any(
        item["hash"] == news_hash
        for item in database
    )


def save_news(news):

    database = load_json(NEWS_DB)

    database.append(news)

    save_json(
        NEWS_DB,
        database
    )

    info("New news saved.")

# ==========================================
# CONTENT
# ==========================================

def content_exists(content_hash):

    database = load_json(CONTENT_DB)

    return any(
        item["hash"] == content_hash
        for item in database
    )


def save_content(content):

    database = load_json(CONTENT_DB)

    database.append(content)

    save_json(
        CONTENT_DB,
        database
    )

    info("Content saved.")

# ==========================================
# REDEEM CODES
# ==========================================

def redeem_exists(code):

    database = load_json(REDEEM_DB)

    return code in database


def save_redeem(code):

    database = load_json(REDEEM_DB)

    database.append(code)

    save_json(
        REDEEM_DB,
        database
    )

    info(f"Redeem code saved: {code}")

# ==========================================
# CACHE
# ==========================================

def load_cache():

    return load_json(CACHE_DB)


def save_cache(data):

    save_json(
        CACHE_DB,
        data
    )

# ==========================================
# CLEAR CACHE
# ==========================================

def clear_cache():

    save_json(
        CACHE_DB,
        []
    )

    info("Cache cleared.")
