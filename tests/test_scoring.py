import unittest
from datetime import datetime

from mvp_bot.scoring.narrative import NarrativeScorer
from mvp_bot.types import NarrativeEvent


class NarrativeScorerTest(unittest.TestCase):
    def test_build_signal_detects_crypto(self):
        scorer = NarrativeScorer()
        events = [
            NarrativeEvent("x", "crypto meme token bull", "a", 100, 50, 20, datetime.utcnow(), {}),
            NarrativeEvent("x", "btc animal meme", "b", 100, 50, 20, datetime.utcnow(), {}),
            NarrativeEvent("x", "eth token moon", "c", 100, 50, 20, datetime.utcnow(), {}),
        ]

        signal = scorer.build_signal(events)

        self.assertEqual(signal.category, "crypto")
        self.assertGreaterEqual(signal.sentiment, 0.5)
        self.assertEqual(signal.mention_count_5m, 3)


if __name__ == "__main__":
    unittest.main()
