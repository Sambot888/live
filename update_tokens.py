import requests
import json

def update_tokens_from_jupiter():
    try:
        # Jupiter API 获取 Solana 上的代币列表
        url = "https://quote-api.jup.ag/v6/tokens"
        response = requests.get(url)
        
        print(f"请求返回状态码: {response.status_code}")  # 打印返回状态码
        
        # 如果返回的数据正常
        if response.status_code == 200:
            tokens = response.json()
            print(f"返回的数据: {tokens}")  # 打印返回数据
            
            cleaned = []
            for token in tokens["tokens"]:
                cleaned.append({
                    "token_address": token["address"],
                    "symbol": token["symbol"],
                    "token_name": token["name"]
                })

            # 存储有效的代币数据
            with open("live.json", "w", encoding="utf-8") as f:
                json.dump(cleaned, f, indent=4, ensure_ascii=False)

            print(f"✅ 已拉取 Jupiter 上线代币共 {len(cleaned)} 条，已写入 live.json")

        else:
            print("[Jupiter] ❌ 请求失败，状态码:", response.status_code)
    except Exception as e:
        print(f"❌ 拉取失败: {str(e)}")

if __name__ == "__main__":
    update_tokens_from_jupiter()
