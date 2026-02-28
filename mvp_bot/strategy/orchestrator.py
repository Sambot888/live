from dataclasses import dataclass
from typing import List

from mvp_bot.config import BotConfig
from mvp_bot.execution.fourmeme_client import FourMemeClient
from mvp_bot.risk.guardrails import RiskGuardrails, RiskState
from mvp_bot.scoring.narrative import NarrativeScorer
from mvp_bot.strategy.take_profit import TakeProfitEngine, TakeProfitStep
from mvp_bot.types import NarrativeEvent


@dataclass
class BotDecision:
    should_create: bool
    reason: str


class NarrativeBotOrchestrator:
    def __init__(self, config: BotConfig, fourmeme: FourMemeClient):
        self.config = config
        self.scorer = NarrativeScorer()
        self.fourmeme = fourmeme
        self.risk = RiskGuardrails(config.max_tokens_per_day, config.stop_loss_pct)
        self.state = RiskState()
        self.take_profit_engine = TakeProfitEngine(
            [TakeProfitStep(level.pnl_pct, level.sell_pct) for level in config.take_profit_levels]
        )

    def decide(self, events: List[NarrativeEvent]) -> BotDecision:
        signal = self.scorer.build_signal(events)

        if signal.category not in self.config.categories:
            return BotDecision(False, f"category_not_allowed:{signal.category}")
        if signal.mention_count_5m < self.config.min_mentions_5m:
            return BotDecision(False, "mentions_too_low")
        if signal.growth_rate < self.config.min_growth_rate:
            return BotDecision(False, "growth_too_low")
        if signal.sentiment < self.config.min_sentiment:
            return BotDecision(False, "sentiment_too_low")
        if not self.risk.can_create(self.state):
            return BotDecision(False, "risk_guardrails_block")

        return BotDecision(True, f"signal_ok:{signal.score}")

    def execute_create_and_buy(self, token_name: str, symbol: str, metadata_uri: str) -> None:
        create_receipt = self.fourmeme.create_token(token_name, symbol, metadata_uri)
        if not create_receipt.ok:
            return
        buy_receipt = self.fourmeme.buy_token(symbol, self.config.target_holding_pct)
        if buy_receipt.ok:
            self.state.tokens_created_today += 1

    def execute_take_profit(self, symbol: str, current_pnl_pct: float) -> None:
        for action in self.take_profit_engine.next_actions(current_pnl_pct):
            self.fourmeme.sell_token(symbol, action.sell_pct, reason=f"pnl_reached_{action.pnl_pct}")
