import argparse
import os

from mvp_bot.collectors.free_sources_collector import FreeSourcesCollector
from mvp_bot.collectors.http_json_collector import HttpJsonCollector
from mvp_bot.collectors.mock_collectors import MockCollector
from mvp_bot.config import load_config
from mvp_bot.execution.fourmeme_client import FourMemeClient
from mvp_bot.strategy.orchestrator import NarrativeBotOrchestrator


def build_collector(mode: str):
    if mode == "http":
        endpoint = os.getenv("NARRATIVE_API_ENDPOINT", "")
        api_key = os.getenv("NARRATIVE_API_KEY", "")
        if not endpoint:
            raise ValueError("NARRATIVE_API_ENDPOINT is required when --mode http")
        return HttpJsonCollector(endpoint=endpoint, api_key=api_key)

    if mode == "free":
        return FreeSourcesCollector()

    return MockCollector(
        source="x",
        samples=[
            "Crypto meme cat token to the moon",
            "今天宠物叙事爆发，链上meme很强",
            "Bullish crypto animal narrative",
            "eth meme bullish",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Narrative bot MVP runner")
    parser.add_argument("--config", default="config/bot.example.json")
    parser.add_argument("--mode", choices=["mock", "http", "free"], default="free")
    parser.add_argument("--symbol", default="ANML")
    parser.add_argument("--name", default="Animal Narrative")
    parser.add_argument("--metadata-uri", default="ipfs://todo-metadata")
    args = parser.parse_args()

    config = load_config(args.config)
    collector = build_collector(args.mode)

    fourmeme = FourMemeClient(
        api_base_url=os.getenv("FOURMEME_API_BASE_URL", "https://api.fourmeme.example"),
        api_key=os.getenv("FOURMEME_API_KEY", "replace-with-env"),
        dry_run=config.dry_run,
    )
    orchestrator = NarrativeBotOrchestrator(config, fourmeme)

    events = collector.fetch_recent()
    if args.mode == "free" and not events:
        print("Free APIs returned no events, fallback to mock samples.")
        events = MockCollector(
            source="fallback",
            samples=["crypto meme cat bullish", "animal token moon", "eth meme narrative"],
        ).fetch_recent()
    decision = orchestrator.decide(events)
    print(f"Decision => create={decision.should_create}, reason={decision.reason}, events={len(events)}")

    if decision.should_create:
        orchestrator.execute_create_and_buy(
            token_name=args.name,
            symbol=args.symbol,
            metadata_uri=args.metadata_uri,
        )
        orchestrator.execute_take_profit(symbol=args.symbol, current_pnl_pct=120)


if __name__ == "__main__":
    main()
