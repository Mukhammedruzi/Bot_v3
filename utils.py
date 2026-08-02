"""
BOT_V3 Utility Functions
Version: 3.0
"""

import re
import hashlib
from datetime import datetime
from pathlib import Path

from logger import info, error

# ==========================================
# TEXT
# ==========================================

def clean_text(text: str) -> str:
    """Matnni tozalash"""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_text(text: str) -> str:
    """Taqqoslash uchun matnni normallashtirish"""
    return clean_text(text).lower()


# ==========================================
# HASH
# ==========================================

def generate_hash(text: str) -> str:
    """SHA256 hash"""
    return hashlib.sha256(
        normalize_text(text).encode("utf-8")
    ).hexdigest()


# ==========================================
# DATE & TIME
# ==========================================

def now():
    """Joriy vaqt"""
    return datetime.now()


def now_string():
    """Joriy vaqt matn ko'rinishida"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==========================================
# FILE
# ==========================================

def ensure_directory(path):
    """Papka yaratish"""
    Path(path).mkdir(
        parents=True,
        exist_ok=True
    )


def file_exists(path):
    return Path(path).exists()


# ==========================================
# REDEEM CODE
# ==========================================

PUBG_PATTERN = re.compile(
    r"[A-Z0-9]{10,20}"
)

MLBB_PATTERN = re.compile(
    r"[A-Z0-9]{10,20}"
)


def extract_pubg_codes(text):
    """PUBG redeem kodlarini ajratish"""
    return list(
        set(PUBG_PATTERN.findall(text.upper()))
    )


def extract_mlbb_codes(text):
    """MLBB redeem kodlarini ajratish"""
    return list(
        set(MLBB_PATTERN.findall(text.upper()))
    )


# ==========================================
# URL
# ==========================================

def is_valid_url(url):
    return url.startswith(
        ("http://", "https://")
    )


# ==========================================
# LOG HELPERS
# ==========================================

def log_success(message):
    info(message)


def log_error(message):
    error(message)
