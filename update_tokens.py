import requests
import json

def update_tokens_from_jupiter():
    try:
        url = "https://quote-api.jup.ag/v6/tokens"
        response = requests.get(url)
        tokens = response.json()

        cleaned = []
        for token in tokens["tokens"]:
            cleaned.append({
                "token_address": token["address"],
                "symbol": token["symbol"],
                "token_name": token["name"]
            })

        # 写入到 live.json
        with open("live.json", "w", encoding="utf-8") as f:
            json.dump(cleaned, f, indent=2, ensure_ascii=False)

        print(f"✅ 已拉取 Jupiter 上线代币共 {len(cleaned)} 条，已写入 live.json")

    except Exception as e:
        print(f"❌ 拉取失败: {str(e)}")

if __name__ == "__main__":
    update_tokens_f
