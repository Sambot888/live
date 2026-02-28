import unittest

from mvp_bot.collectors.free_sources_collector import FreeSourcesCollector


class FreeSourcesCollectorParsingTest(unittest.TestCase):
    def test_parse_reddit_payload(self):
        payload = {
            "data": {
                "children": [
                    {
                        "data": {
                            "title": "cat meme coin is mooning",
                            "author": "bob",
                            "ups": 88,
                            "num_crossposts": 3,
                            "num_comments": 9,
                            "created_utc": 1700000000,
                            "subreddit": "CryptoCurrency",
                        }
                    }
                ]
            }
        }
        events = FreeSourcesCollector.parse_reddit_payload(payload)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].source, "reddit")
        self.assertIn("cat meme", events[0].text)

    def test_parse_coingecko_payload(self):
        payload = {
            "coins": [
                {"item": {"name": "Dogecoin", "symbol": "DOGE", "score": 7, "market_cap_rank": 9}}
            ]
        }
        events = FreeSourcesCollector.parse_coingecko_payload(payload)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].source, "coingecko")
        self.assertIn("Dogecoin", events[0].text)


if __name__ == "__main__":
    unittest.main()
