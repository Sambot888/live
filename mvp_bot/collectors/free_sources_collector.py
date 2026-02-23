from __future__ import annotations

import json
from datetime import datetime
from typing import List
from urllib.error import URLError
from urllib.request import Request, urlopen

from mvp_bot.collectors.base import BaseCollector
from mvp_bot.types import NarrativeEvent


class FreeSourcesCollector(BaseCollector):
    """Collect narrative signals from free/public endpoints.

    Sources:
    - Reddit JSON feeds (r/CryptoCurrency, r/memes, r/aww)
    - CoinGecko trending coins endpoint
    """

    REDDIT_URLS = [
        "https://www.reddit.com/r/CryptoCurrency/hot.json?limit=20",
        "https://www.reddit.com/r/memes/hot.json?limit=20",
        "https://www.reddit.com/r/aww/hot.json?limit=20",
    ]
    COINGECKO_TRENDING_URL = "https://api.coingecko.com/api/v3/search/trending"

    def __init__(self, timeout_seconds: int = 8):
        self.timeout_seconds = timeout_seconds

    def fetch_recent(self) -> List[NarrativeEvent]:
        events: List[NarrativeEvent] = []
        events.extend(self._fetch_reddit())
        events.extend(self._fetch_coingecko())
        return events

    def _fetch_reddit(self) -> List[NarrativeEvent]:
        headers = {
            "Accept": "application/json",
            "User-Agent": "narrative-bot-mvp/0.1",
        }
        events: List[NarrativeEvent] = []
        for url in self.REDDIT_URLS:
            payload = _fetch_json(url, headers=headers, timeout=self.timeout_seconds)
            events.extend(self.parse_reddit_payload(payload))
        return events

    def _fetch_coingecko(self) -> List[NarrativeEvent]:
        payload = _fetch_json(self.COINGECKO_TRENDING_URL, headers={"Accept": "application/json"}, timeout=self.timeout_seconds)
        return self.parse_coingecko_payload(payload)

    @staticmethod
    def parse_reddit_payload(payload: object) -> List[NarrativeEvent]:
        if not isinstance(payload, dict):
            return []
        children = payload.get("data", {}).get("children", [])
        if not isinstance(children, list):
            return []

        out: List[NarrativeEvent] = []
        for child in children:
            data = child.get("data", {}) if isinstance(child, dict) else {}
            title = str(data.get("title", "")).strip()
            if not title:
                continue
            created_utc = data.get("created_utc", 0)
            created_at = datetime.utcfromtimestamp(created_utc) if isinstance(created_utc, (int, float)) else datetime.utcnow()
            out.append(
                NarrativeEvent(
                    source="reddit",
                    text=title,
                    author=str(data.get("author", "unknown")),
                    likes=int(data.get("ups", 0)),
                    shares=int(data.get("num_crossposts", 0)),
                    comments=int(data.get("num_comments", 0)),
                    created_at=created_at,
                    metadata={"subreddit": str(data.get("subreddit", ""))},
                )
            )
        return out

    @staticmethod
    def parse_coingecko_payload(payload: object) -> List[NarrativeEvent]:
        if not isinstance(payload, dict):
            return []
        coins = payload.get("coins", [])
        if not isinstance(coins, list):
            return []

        out: List[NarrativeEvent] = []
        for wrapped in coins:
            item = wrapped.get("item", {}) if isinstance(wrapped, dict) else {}
            name = str(item.get("name", "")).strip()
            symbol = str(item.get("symbol", "")).strip()
            market_cap_rank = item.get("market_cap_rank")
            if not name:
                continue
            text = f"trending coin {name} {symbol} crypto meme narrative"
            out.append(
                NarrativeEvent(
                    source="coingecko",
                    text=text,
                    author="coingecko",
                    likes=int(item.get("score", 0)) + 1,
                    shares=0,
                    comments=0,
                    created_at=datetime.utcnow(),
                    metadata={"market_cap_rank": str(market_cap_rank)},
                )
            )
        return out


def _fetch_json(url: str, headers: dict, timeout: int) -> object:
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (URLError, json.JSONDecodeError, TimeoutError, ValueError):
        return {}
