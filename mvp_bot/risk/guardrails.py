from dataclasses import dataclass


@dataclass
class RiskState:
    tokens_created_today: int = 0
    daily_pnl_pct: float = 0.0


class RiskGuardrails:
    def __init__(self, max_tokens_per_day: int, daily_loss_limit_pct: float):
        self.max_tokens_per_day = max_tokens_per_day
        self.daily_loss_limit_pct = daily_loss_limit_pct

    def can_create(self, state: RiskState) -> bool:
        if state.tokens_created_today >= self.max_tokens_per_day:
            return False
        if state.daily_pnl_pct <= -abs(self.daily_loss_limit_pct):
            return False
        return True
