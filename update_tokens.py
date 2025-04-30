
import requests
import json

def fetch_from_proxy():
    url = "https://gmgn-proxy.up.railway.app/live.json"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"[gmgn_proxy] Fetch failed: {response.status_code}")
        return []

    return response.json()

if __name__ == "__main__":
    data = fetch_from_proxy()
    if data:
        with open("live.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"[gmgn_proxy] ✅ Pulled {len(data)} tokens from mirror")
    else:
        print("[gmgn_proxy] No data pulled.")

