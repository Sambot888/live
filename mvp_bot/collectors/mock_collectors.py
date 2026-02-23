from datetime import datetime
from typing import List

from mvp_bot.collectors.base import BaseCollector
from mvp_bot.types import NarrativeEvent


class MockCollector(BaseCollector):
    def __init__(self, source: str, samples: List[str]):
        self.source = source
        self.samples = samples

    def fetch_recent(self) -> List[NarrativeEvent]:
        now = datetime.utcnow()
        return [
            NarrativeEvent(
                source=self.source,
                text=text,
                author=f"{self.source}_author_{idx}",
                likes=100 + idx * 10,
                shares=30 + idx,
                comments=15 + idx,
                created_at=now,
                metadata={"lang": "zh"},
            )
            for idx, text in enumerate(self.samples)
        ]
