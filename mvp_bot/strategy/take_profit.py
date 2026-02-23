from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TakeProfitStep:
    pnl_pct: float
    sell_pct: float


class TakeProfitEngine:
    def __init__(self, steps: List[TakeProfitStep]):
        self.steps = sorted(steps, key=lambda step: step.pnl_pct)
        self.executed = set()

    def next_actions(self, current_pnl_pct: float) -> List[TakeProfitStep]:
        actions = []
        for index, step in enumerate(self.steps):
            if index in self.executed:
                continue
            if current_pnl_pct >= step.pnl_pct:
                actions.append(step)
                self.executed.add(index)
        return actions
