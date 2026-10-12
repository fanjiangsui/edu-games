# 🍉 西瓜飛鏢 (Watermelon Darts)

瞄準旋轉中的西瓜，把物品安全插上外圈，挑戰三個關卡。撞到之前插上的物品就要重來。

**線上玩：** `https://<你的帳號>.github.io/<入口repo>/games/watermelon-darts/`

## 玩法
- 三關：第 1 關 6 支、第 2 關 8 支、第 3 關 10 支，轉速和換向頻率逐關提高
- 可選發射物：飛鏢、口紅、刀子、鉛筆、吸管（各自的碰撞間隔不同）
- 操作：點「發射」按鈕、點畫面，或按空白鍵

## 技術
- 單一檔案 `index.html`（HTML + CSS + JavaScript，Canvas 繪圖）
- 無外部依賴、無打包流程，直接用瀏覽器開啟即可
- 本機預覽：`python3 -m http.server` 後開 http://localhost:8000

## 製作紀錄
- v0.1：由 ChatGPT 協作產生初版；由燧整理並放上 GitHub

## 之後可以進化
- [ ] 最高分／最佳通關時間（localStorage）
- [ ] 音效與震動回饋
- [ ] 更多關卡或無盡模式
- [ ] 拆成 `index.html` / `style.css` / `game.js`
- [ ] 其他西瓜造型或主題
