from collections import Counter
from typing import Iterable

from mvp_bot.types import NarrativeEvent, NarrativeSignal

CATEGORY_KEYWORDS = {
    "animal": ["cat", "dog", "熊猫", "宠物", "animal"],
    "crypto": ["btc", "eth", "meme", "token", "链上", "crypto"],
}


class NarrativeScorer:
    def classify_category(self, text: str) -> str:
        lower = text.lower()
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(keyword in lower for keyword in keywords):
                return category
        return "other"

    def sentiment_score(self, event: NarrativeEvent) -> float:
        positive_tokens = ["moon", "bull", "看涨", "冲", "利好"]
        negative_tokens = ["rug", "scam", "暴跌", "看空"]

        lower = event.text.lower()
        pos = sum(token in lower for token in positive_tokens)
        neg = sum(token in lower for token in negative_tokens)

        base = 0.5 + 0.15 * pos - 0.2 * neg
        return max(0.0, min(1.0, base))

    def build_signal(self, events: Iterable[NarrativeEvent]) -> NarrativeSignal:
        event_list = list(events)
        if not event_list:
            return NarrativeSignal("other", 0.0, 0.0, 0, 0.0)

        categories = [self.classify_category(item.text) for item in event_list]
        category = Counter(categories).most_common(1)[0][0]

        mention_count = len(event_list)
        avg_sentiment = sum(self.sentiment_score(item) for item in event_list) / mention_count

        interactions = sum(item.likes + item.shares + item.comments for item in event_list)
        velocity = interactions / max(mention_count, 1)
        growth_rate = 1.0 + min(3.0, velocity / 500.0)

        score = 0.4 * mention_count + 0.25 * growth_rate + 0.35 * avg_sentiment
        return NarrativeSignal(
            category=category,
            score=round(score, 4),
            sentiment=round(avg_sentiment, 4),
            mention_count_5m=mention_count,
            growth_rate=round(growth_rate, 4),
        )
