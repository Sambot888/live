from __future__ import annotations

import json
from datetime import datetime
from urllib.error import URLError
from urllib.request import Request, urlopen
from typing import List

from mvp_bot.collectors.base import BaseCollector
from mvp_bot.types import NarrativeEvent


class HttpJsonCollector(BaseCollector):
    """Fetch events from a JSON HTTP endpoint.

    Expected response shape:
    {
      "items": [
        {
          "text": "...",
          "author": "...",
          "likes": 1,
          "shares": 2,
          "comments": 3,
          "created_at": "2026-01-01T00:00:00Z",
          "source": "x"
        }
      ]
    }
    """

    def __init__(self, endpoint: str, api_key: str = "", timeout_seconds: int = 8):
        self.endpoint = endpoint
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    def fetch_recent(self) -> List[NarrativeEvent]:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        request = Request(self.endpoint, headers=headers)
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except URLError:
            return []

        items = payload.get("items", []) if isinstance(payload, dict) else []
        events: List[NarrativeEvent] = []

        for item in items:
            if not isinstance(item, dict):
                continue
            created_raw = item.get("created_at", "")
            created_at = _parse_datetime(created_raw)
            events.append(
                NarrativeEvent(
                    source=str(item.get("source", "api")),
                    text=str(item.get("text", "")),
                    author=str(item.get("author", "unknown")),
                    likes=int(item.get("likes", 0)),
                    shares=int(item.get("shares", 0)),
                    comments=int(item.get("comments", 0)),
                    created_at=created_at,
                    metadata={"collector": "http_json"},
                )
            )

        return events


def _parse_datetime(raw: str) -> datetime:
    if not raw:
        return datetime.utcnow()
    normalized = raw.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return datetime.utcnow()
