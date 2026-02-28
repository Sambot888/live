from dataclasses import dataclass
from pathlib import Path
from typing import List
import json


@dataclass(frozen=True)
class TakeProfitLevel:
    pnl_pct: float
    sell_pct: float


@dataclass(frozen=True)
class BotConfig:
    categories: List[str]
    min_mentions_5m: int
    min_growth_rate: float
    min_sentiment: float
    target_holding_pct: float
    max_tokens_per_day: int
    stop_loss_pct: float
    take_profit_levels: List[TakeProfitLevel]
    trailing_enabled: bool
    trail_pct: float
    dry_run: bool


def load_config(path: str = "config/bot.example.json") -> BotConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    take_profit_levels = [
        TakeProfitLevel(level["pnl_pct"], level["sell_pct"])
        for level in data["take_profit"]["levels"]
    ]

    return BotConfig(
        categories=data["narrative"]["categories"],
        min_mentions_5m=data["narrative"]["min_mentions_5m"],
        min_growth_rate=data["narrative"]["min_growth_rate"],
        min_sentiment=data["narrative"]["min_sentiment"],
        target_holding_pct=data["execution"]["target_holding_pct"],
        max_tokens_per_day=data["risk"]["max_tokens_per_day"],
        stop_loss_pct=data["risk"]["stop_loss_pct"],
        take_profit_levels=take_profit_levels,
        trailing_enabled=data["take_profit"]["trailing"]["enabled"],
        trail_pct=data["take_profit"]["trailing"]["trail_pct"],
        dry_run=data["execution"].get("dry_run", True),
    )
