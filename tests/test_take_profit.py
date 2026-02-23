import unittest

from mvp_bot.strategy.take_profit import TakeProfitEngine, TakeProfitStep


class TakeProfitEngineTest(unittest.TestCase):
    def test_progressive_triggers_only_once(self):
        engine = TakeProfitEngine(
            [TakeProfitStep(50, 20), TakeProfitStep(100, 20), TakeProfitStep(200, 30)]
        )

        first = engine.next_actions(120)
        second = engine.next_actions(120)

        self.assertEqual([step.pnl_pct for step in first], [50, 100])
        self.assertEqual(second, [])


if __name__ == "__main__":
    unittest.main()
