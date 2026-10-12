# edu-games 入口 repo：協作規則

這個 repo 是 GitHub Pages 的遊戲入口（https://fanjiangsui.github.io/edu-games/）。用戶說「加一個新遊戲」時，照下面做。

## 加新遊戲

- 新遊戲放 `games/<名稱>/`（英文小寫加連字號），放進 `index.html`（單檔遊戲）或 `build_game.py`（需要打包的遊戲），再加一份 `game.json`。
- 入口頁卡片格式比照現有卡片：卡片由 `build_all.py` 讀各遊戲的 `game.json` 自動產生，不手寫 HTML。`game.json` 欄位：`title`、`description`、`icon`（一個 emoji）、`group`（`玩一局` 或 `腦袋補給站`）、`audience`、`note`、`status`。
- 遊戲原始檔照原樣放入，不改遊戲邏輯。若「← 首頁」按鈕擠壞版面，用 `game.json` 的 `inject_css` 只改打包輸出。
- 不動其他遊戲的檔案。

## 統一入口原則（Sui 2026-10-12 決定）

- 以後新增的遊戲或 App（小工具、PWA 都算），預設都整理進這個入口，不另開新 repo：放 `games/<名稱>/`，首頁自動出現卡片。
- 分區用 `game.json` 的 `group`：`玩一局`、`腦袋補給站`；內容不屬於這兩類時，可以新增分區名稱，先跟 Sui 確認名稱。
- 例外：`think-lenses`（思考鏡頭）已經獨立上線在 https://fanjiangsui.github.io/think-lenses/ ，維持原網址；要不要搬進入口會改變已分享的連結，先問 Sui 再動。
- 若某個 App 需要獨立 repo（例如要自己的網域或權限），先問 Sui，不自行決定。

## 打包與檢查

- 改完跑 `python3 build_all.py`（成語資料檢查需要較新的 `jsonschema`，系統已升到 4.x）。
- 用 `python3 -m http.server` 從入口頁點進新遊戲，確認路徑與離線清單都正常。
- 更新 `README.md` 的遊戲表格。

## 提交

- **commit 前先給用戶看 `git diff` 摘要**，用戶確認後才 commit。
- 不自動 push；push 前再問一次。
- 用 `git add` 指定檔案，不用 `git add -A`。
- commit 作者用 `fanjiangsui@hotmail.com`（全域設定是公司信箱，不要用）：若 `git config user.email` 不是這個，先在這個 repo 內設定。

## 注意

- 同一個網域（`fanjiangsui.github.io`）下所有頁面共用瀏覽器儲存空間，新遊戲的 localStorage key 不要和既有的衝突：`mm-prefs`、`chengyu-tts-check-v2`。
- 網址路徑已經分享出去，不搬動或改名既有遊戲資料夾。
