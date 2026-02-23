# Narrative Bot MVP Skeleton

## 可以直接运行吗？
可以。默认模式已改成 `--mode free`（免费公开 API），且 `dry_run=true`，不会真实下单。

```bash
python -m mvp_bot.main
python -m unittest discover -s tests
```

## 已接入的免费公开数据源（无需你先给 API）
- Reddit 热门帖子：`r/CryptoCurrency`、`r/memes`、`r/aww`
- CoinGecko 热门币：`/api/v3/search/trending`

> 说明：这些公开源可先跑通“抓取 → 评分 → 决策”流程，后续再替换成你指定的微博/抖音/X 数据供应商。

## 还可以做什么（下一步）
- 把 `--mode http` 接入你指定的商业/私有热点 API。
- 把 `FourMemeClient` 的占位逻辑替换成真实 SDK/API 签名交易。
- 加回测、资金曲线、风控告警（如 Telegram/飞书）。

## 需要你提供哪些 API（做实盘时）
1. 热点数据 API 文档（字段、频率限制、鉴权方式）
2. FourMeme 官方 API/SDK 文档（创建代币、买入、卖出）
3. 链上参数（RPC、滑点、gas、私钥托管方案）

## 现在需要做什么（按顺序）
1. **先确认本地能跑通**  
   - Linux/macOS: `./run_mvp.sh free`  
   - Windows: `run_mvp.bat free`
2. **决定你的数据输入路径**  
   - 先用 `free` 模式验证流程；
   - 如果你有自己的热点数据 API，改用 `http` 模式并配置环境变量。
3. **调整策略参数（最重要）**  
   - 编辑 `config/bot.example.json` 里的阈值：`min_mentions_5m`、`min_sentiment`、`take_profit.levels`。
4. **接入真实交易前的强制检查**  
   - 仍保持 `dry_run=true`，观察至少 1~3 天信号质量；
   - 统计触发频率、误报率、止盈命中情况。
5. **准备实盘对接资料**  
   - FourMeme API/SDK 文档；
   - 钱包签名方案（建议 KMS/HSM）；
   - 链参数（RPC、滑点、gas 上限）。

> 结论：你现在最该做的是 **先跑通 free 模式 + 调参数**，而不是立刻上实盘。

## 一键运行脚本

> 你要的“一个可以直接运行的脚本”：

```bash
python run_mvp.py
```

可选参数：
```bash
python run_mvp.py --mode free
python run_mvp.py --mode mock
python run_mvp.py --mode http
python run_mvp.py --mode free --skip-tests
```


### Linux / macOS
```bash
./run_mvp.sh
```
可选模式参数：
```bash
./run_mvp.sh free
./run_mvp.sh mock
./run_mvp.sh http
```

### Windows
```bat
run_mvp.bat
```
可选模式参数：
```bat
run_mvp.bat free
run_mvp.bat mock
run_mvp.bat http
```

## 运行模式
### 1) 免费公开源模式（默认）
```bash
python -m mvp_bot.main --mode free
```

### 2) Mock 模式（离线演示）
```bash
python -m mvp_bot.main --mode mock
```

### 3) HTTP 模式（接你自己的 API）
```bash
export NARRATIVE_API_ENDPOINT="https://your-provider.example/api/v1/hot"
export NARRATIVE_API_KEY="your_key"
python -m mvp_bot.main --mode http
```

接口响应约定：
```json
{
  "items": [
    {
      "text": "crypto meme cat token moon",
      "author": "user_1",
      "likes": 100,
      "shares": 20,
      "comments": 10,
      "created_at": "2026-01-01T00:00:00Z",
      "source": "x"
    }
  ]
}
```

## Structure
- `mvp_bot/collectors`: 数据采集适配器（free/http/mock）。
- `mvp_bot/scoring`: 叙事分类、情绪、评分模型。
- `mvp_bot/execution`: FourMeme 客户端占位实现（默认 dry-run）。
- `mvp_bot/risk`: 每日风控闸门。
- `mvp_bot/strategy`: 编排和分批止盈。
- `config/bot.example.json`: 可调参数模板。

## GitHub 推送（按你的用户名：`Sambot888`）
如果你在 GitHub 上创建的仓库名是 `live`，直接复制执行：

```bash
git remote add origin https://github.com/Sambot888/live.git
git push -u origin work
```

如果你想改成 `main` 分支：

```bash
git branch -M main
git push -u origin main
```


### 用脚本自动配置 GitHub 远程（Sambot888）
```bash
python setup_github_remote.py
# 然后执行：
# git push -u origin work
```

如果你要切到 main：
```bash
python setup_github_remote.py --set-main
# 然后执行：
# git push -u origin main
```
