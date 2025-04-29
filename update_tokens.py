
import requests
import json
import os

URL = "https://api.dexscreener.com/token-profiles/latest/v1"
OUTPUT_PATH = "live.json"

print("[SAMBOT-MIRROR] Running update_tokens.py...")

try:
    response = requests.get(URL, timeout=10)
    if response.status_code != 200:
        print(f"[gmgn_proxy] Fetch failed: {response.status_code}")
        print("[gmgn_proxy] No data pulled.")
        exit()

    raw_data = response.json()
    if not isinstance(raw_data, list) or len(raw_data) == 0:
        print("[gmgn_proxy] Empty or invalid token list.")
        exit()

    tokens = []
    for item in raw_data:
        address = item.get("address") or item.get("tokenAddress") or ""
        symbol = item.get("symbol") or ""
        name = item.get("name") or ""

        if address.strip() and symbol.strip() and name.strip():
            tokens.append({
                "token_address": address,
                "symbol": symbol,
                "token_name": name
            })

    if not tokens:
        print("[gmgn_proxy] ❌ No valid tokens extracted.")
        exit()

    print(f"[gmgn_proxy] ✅ Extracted {len(tokens)} valid tokens from DEXScreener")

    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
        if existing == tokens:
            print("[SAMBOT-MIRROR] No change detected in live.json")
            exit()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)

    print("[SAMBOT-MIRROR] ✅ live.json updated.")

except Exception as e:
    print("[gmgn_proxy] ❌ Exception:", str(e))
