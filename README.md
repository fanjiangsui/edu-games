# edu-games 學習小遊戲

給孩子玩的離線學習遊戲集合，網址：https://fanjiangsui.github.io/edu-games/

| 遊戲 | 路徑 | 說明 |
|---|---|---|
| 成語小達人 | `games/chinese-idiom/` | 500 個常用成語，注音、故事、計時計分 |
| 話匣子 | `games/talkbox/` | 中英雙語聊天卡 670 題＋30 張挑戰卡，可安裝成 PWA 離線用（題庫改 `parts/*.txt`，見該資料夾 README） |
| 西瓜飛鏢 | `games/watermelon-darts/` | 瞄準旋轉的西瓜，避開舊物品，三關挑戰（單檔 Canvas 遊戲） |

## 結構

```
games/<遊戲>/      每個遊戲的資料與工具（game.json 是遊戲資訊）
docs/              打包結果，GitHub Pages 發佈這個資料夾
build_all.py       檢查並打包所有遊戲、產生首頁
```

## 更新流程

1. 修改 `games/<遊戲>/data/` 裡的資料（例如修正讀音、`tts-overrides.json` 朗讀同音字）
2. `python3 build_all.py`（會自動合併、檢查、打包；檢查有錯就不會打包）
3. commit 並 push，GitHub Pages 約 1～2 分鐘後更新

新增遊戲：在 `games/` 開一個資料夾，放 `game.json`，再放一個 `index.html`（單檔遊戲）或 `build_game.py`（需要打包的遊戲）。詳見 `build_all.py` 開頭說明。

需要 Python 3；資料格式檢查若要完整，需 `pip install jsonschema`。

## 說明

- 內容由 AI（Claude）協助產生與整理，未逐條人工校對；出處與典故標示「推測」或「待查」的部分不是事實陳述。
- 難度「入門／進階／高階」是遊戲自訂分級，不是教育部的年級規定。
