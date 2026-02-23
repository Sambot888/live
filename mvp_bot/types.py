from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class NarrativeEvent:
    source: str
    text: str
    author: str
    likes: int
    shares: int
    comments: int
    created_at: datetime
    metadata: Dict[str, str]


@dataclass(frozen=True)
class NarrativeSignal:
    category: str
    score: float
    sentiment: float
    mention_count_5m: int
    growth_rate: float
