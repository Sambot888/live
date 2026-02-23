from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class TxReceipt:
    tx_hash: str
    ok: bool
    details: Dict[str, str]


class FourMemeClient:
    def __init__(self, api_base_url: str, api_key: str, dry_run: bool = True):
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.dry_run = dry_run

    def create_token(self, name: str, symbol: str, metadata_uri: str) -> TxReceipt:
        if self.dry_run:
            return TxReceipt("dryrun-create", True, {"name": name, "symbol": symbol})
        raise NotImplementedError("Connect to FourMeme API/SDK here.")

    def buy_token(self, symbol: str, target_holding_pct: float) -> TxReceipt:
        if self.dry_run:
            return TxReceipt("dryrun-buy", True, {"symbol": symbol, "target": str(target_holding_pct)})
        raise NotImplementedError("Connect to FourMeme API/SDK here.")

    def sell_token(self, symbol: str, sell_pct: float, reason: Optional[str] = None) -> TxReceipt:
        if self.dry_run:
            return TxReceipt("dryrun-sell", True, {"symbol": symbol, "sell_pct": str(sell_pct), "reason": reason or ""})
        raise NotImplementedError("Connect to FourMeme API/SDK here.")
