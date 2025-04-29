
import requests
import re
import json

def fetch_gmgn_tokens():
    url = "https://gmgn.ai/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"[gmgn_mirror] Failed to fetch HTML: {response.status_code}")
        return []

    html = response.text

    # 抓取 token_address、symbol、token_name 列表（匹配数组）
    pattern = re.compile(r'"token_address":"(.*?)".*?"symbol":"(.*?)".*?"token_name":"(.*?)"', re.DOTALL)
    matches = pattern.findall(html)

    tokens = []
    for token_address, symbol, token_name in matches:
        tokens.append({
            "token_address": token_address,
            "symbol": symbol,
            "token_name": token_name
        })

    return tokens

if __name__ == "__main__":
    tokens = fetch_gmgn_tokens()
    if tokens:
        with open("live.json", "w", encoding="utf-8") as f:
            json.dump(tokens, f, indent=2)
        print(f"[gmgn_mirror] ✅ Updated live.json with {len(tokens)} tokens")
    else:
        print("[gmgn_mirror] No tokens fetched.")
