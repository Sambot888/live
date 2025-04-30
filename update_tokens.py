import requests
import json
import os

def update_tokens_from_jupiter():
    try:
        # Jupiter API 获取 Solana 上的代币列表
        url = "https://quote-api.jup.ag/v6/tokens"
        response = requests.get(url)

        # 打印请求状态码
        print(f"请求返回状态码: {response.status_code}")

        # 如果请求成功
        if response.status_code == 200:
            tokens = response.json()

            # 确保返回的数据包含 'tokens'
            if "tokens" not in tokens:
                print("❌ API 返回的数据中没有 'tokens' 键，请检查返回格式")
                return

            cleaned = []
            for token in tokens["tokens"]:
                # 打印每个代币信息，检查数据格式
                print(f"代币地址: {token['address']} | 符号: {token['symbol']} | 名称: {token['name']}")
                cleaned.append({
                    "token_address": token["address"],
                    "symbol": token["symbol"],
                    "token_name": token["name"]
                })

            # 确保路径正确，写入到桌面
            desktop_path = "C:/Users/Administrator/Desktop/live_test.json"
            if not os.path.exists(desktop_path):
                print(f"❌ 无法找到桌面路径 {desktop_path}，请检查路径是否正确。")
                return

            # 将数据写入桌面文件
            with open(desktop_path, "w", encoding="utf-8") as f:
                json.dump(cleaned, f, indent=4, ensure_ascii=False)

            print(f"✅ 成功写入 {len(cleaned)} 条代币数据到桌面文件：{desktop_path}")

        else:
            print("❌ 请求失败，状态码:", response.status_code)

    except Exception as e:
        print(f"❌ 错误发生: {str(e)}")

if __name__ == "__main__":
    update_tokens_from_jupiter()
