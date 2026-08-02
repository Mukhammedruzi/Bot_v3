"""
BOT_V3 Scanner Engine
Version: 3.0

Main Scanner Module
"""

import asyncio
import aiohttp
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from googleapiclient.discovery import build
from tenacity import retry, stop_after_attempt, wait_fixed

from config import *
from logger import info, warning, error
from database import (
    create_hash,
    news_exists,
    save_news,
    redeem_exists,
    save_redeem,
)
from utils import (
    clean_text,
    extract_pubg_codes,
    extract_mlbb_codes,
    now_string,
)

# ==========================================
# MAIN CLASS
# ==========================================

class Scanner:

    def __init__(self):

        self.youtube = build(
            "youtube",
            "v3",
            developerKey=YOUTUBE_API_KEY
        )

        self.session = requests.Session()

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "BOT_V3 AI Scanner"
            )
        }

        self.timeout = 30

        self.news = []

        self.redeem_codes = []

        info("Scanner initialized.")

    # ======================================

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(5)
    )
    def get(self, url):

        response = self.session.get(
            url,
            headers=self.headers,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.text

    # ======================================

    def parse_html(self, html):

        return BeautifulSoup(
            html,
            "lxml"
        )

    # ======================================

    def add_news(
        self,
        title,
        source,
        url,
        content=""
    ):

        title = clean_text(title)

        uid = create_hash(title)

        if news_exists(uid):
            return

        item = {

            "hash": uid,

            "title": title,

            "source": source,

            "url": url,

            "content": clean_text(content),

            "created_at": now_string()

        }

        save_news(item)

        self.news.append(item)

        info(f"News Added: {title}")
 # ======================================

 def add_redeem(self, code):

      code = code.strip().upper()

      if redeem_exists(code):
         return

         save_redeem(code)

         self.redeem_codes.append(code)

         info(f"Redeem Code: {code}")
# ======================================
# RSS NEWS SCANNER
# ======================================

def scan_rss(self):

    info("RSS scan started.")

    for source in NEWS_SOURCES:

        try:

            feed = feedparser.parse(source)

            for entry in feed.entries:

                title = entry.get("title", "")

                link = entry.get("link", "")

                summary = entry.get("summary", "")

                self.add_news(
                    title=title,
                    source=source,
                    url=link,
                    content=summary
                )

                text = (
                    title + " " + summary
                )

                for code in extract_pubg_codes(text):
                    self.add_redeem(code)

                for code in extract_mlbb_codes(text):
                    self.add_redeem(code)

        except Exception as e:

            error(f"RSS Error: {e}")

# ======================================
# WEBSITE SCANNER
# ======================================

def scan_website(
    self,
    url
):

    try:

        html = self.get(url)

        soup = self.parse_html(html)

        text = soup.get_text(" ")

        for code in extract_pubg_codes(text):

            self.add_redeem(code)

        for code in extract_mlbb_codes(text):

            self.add_redeem(code)

        self.add_news(

            title=soup.title.text if soup.title else url,

            source=url,

            url=url,

            content=text[:1000]

        )

    except Exception as e:

        error(f"Website Error: {e}")
# ======================================
# YOUTUBE SCANNER
# ======================================

def scan_youtube(self, query, max_results=10):

    info(f"YouTube Scan: {query}")

    try:

        request = self.youtube.search().list(

            part="snippet",

            q=query,

            type="video",

             maxResults=max_results,

             order="date"

        )

        response = request.execute()

        for item in response.get("items", []):

                 video_id = item["id"]["videoId"]

                 snippet = item["snippet"]

                 title = clean_text(
                           snippet.get("title", "")
                 )

                description = clean_text(
                    snippet.get("description", "")
                )

                url = (
                    f"https://www.youtube.com/watch?v={video_id}"
                )

                self.add_news(

                    title=title,

                    source="YouTube",

                    url=url,

                    content=description

                )

                text = (
                    title + " " + description
                )

                for code in extract_pubg_codes(text):

                    self.add_redeem(code)

                for code in extract_mlbb_codes(text):

                    self.add_redeem(code)

        except Exception as e:

            error(f"YouTube Scan Error: {e}")

    # ======================================
    # ALL SOURCES
    # ======================================

    def scan_all(self):

        info("Full scan started.")

        self.scan_rss()

        for site in WEBSITE_SOURCES:

            self.scan_website(site)

        for keyword in SEARCH_KEYWORDS:

            self.scan_youtube(keyword)

        info("Full scan finished.")
    
    # ======================================
    # CONTENT VALIDATOR
    # ======================================

    def validate_news(self):

        info("Validating news...")

        valid_news = []

        for item in self.news:

            title = clean_text(
                item.get("title", "")
            )

            content = clean_text(
                item.get("content", "")
            )

            if len(title) < 8:
                continue

            if len(content) < 20:
                continue

            valid_news.append(item)

        self.news = valid_news

        info(
            f"Valid News: {len(self.news)}"
        )

    # ======================================
    # REMOVE DUPLICATES
    # ======================================

    def remove_duplicates(self):

        unique = {}

        for item in self.news:

            key = create_hash(
                item["title"]
            )

            unique[key] = item

        self.news = list(
            unique.values()
        )

        info(
            f"Unique News: {len(self.news)}"
        )

    # ======================================
    # SUMMARY
    # ======================================

    def summary(self):

        return {

            "news_count": len(
                self.news
            ),

            "redeem_count": len(
                self.redeem_codes
            ),

            "time": now_string()

        }

    # ======================================
    # PROCESS
    # ======================================

    def process(self):

        self.remove_duplicates()

        self.validate_news()

        result = self.summary()

        info(
            f"Scanner Finished | "
            f"News={result['news_count']} | "
            f"Redeem={result['redeem_count']}"
        )

        return result
        # ======================================
    # INTERNET CHECK
    # ======================================

    def check_connection(self):

        try:

            requests.get(

                "https://www.google.com",

                timeout=5

            )

            return True

        except Exception:

            return False

    # ======================================
    # ASYNC SCAN
    # ======================================

    async def async_scan(self):

        loop = asyncio.get_running_loop()

        await loop.run_in_executor(

            None,

            self.scan_all

        )

    # ======================================
    # RUN
    # ======================================

    async def run(self):

        info("BOT_V3 Scanner Started")

        if not self.check_connection():

            error("Internet Connection Failed")

            return

        await self.async_scan()

        result = self.process()

        info("BOT_V3 Scanner Finished")

        return result

    # ======================================
    # RESET
    # ======================================

    def reset(self):

        self.news.clear()

        self.redeem_codes.clear()

        info("Scanner Cache Cleared")
# ======================================
# MAIN
# ======================================

async def main():

    scanner = Scanner()

    result = await scanner.run()

    print(result)


# ======================================
# START
# ======================================

if __name__ == "__main__":

    asyncio.run(main())
