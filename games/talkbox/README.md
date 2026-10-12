# 話匣子 Talk Box (PWA)

中英雙語聊天卡：670 題 + 30 張挑戰卡，可依對象（親子／朋友）、等級（暖身／聊聊／走心）、類型篩選，
另有「練英文」模式。純靜態網站，不需要後端，安裝後可離線使用。

## 檔案
- `index.html` 主程式（單檔，無外部資源，系統字型）
- `questions.js` 題庫（由 `build_questions.js` 產生，請勿手改）
- `parts/*.txt` 題庫原始檔，格式 `對象|類型|中文|English`（對象：`f` 親子、`p` 朋友、`fp` 兩者）
- `sw.js` 離線快取；`manifest.webmanifest` 安裝設定；`icons/` 圖示
- `build_questions.js` 合併並檢查題庫；`make_icons.py` 產生圖示

## 部署到 GitHub Pages
1. 把整個資料夾放進你的 repo（例如 `talkbox/`），或單獨建一個 repo。
2. Settings → Pages → 選分支與資料夾。網址會是 `https://<帳號>.github.io/<repo>/`（或 `/talkbox/`）。
3. 所有路徑都是相對路徑，放在子目錄也能運作。PWA 必須走 HTTPS，GitHub Pages 預設就是。

## 安裝到手機
- Android（Chrome）：開啟網址 → 右上角「安裝到手機」按鈕，或選單 → 安裝應用程式。
- iPhone（Safari）：分享 → 加入主畫面。

## 更新題庫
1. 編輯 `parts/*.txt`，然後執行 `node build_questions.js`（會檢查欄位、重複題、類型是否正確）。
2. 把 `sw.js` 的 `VERSION` 改成新版本號（例如 `talkbox-v2`）。
3. 推上 GitHub。手機端會在下次開啟時更新（第二次開啟生效）。

## 本機測試
`python3 -m http.server 8000` 後開 `http://localhost:8000`。Service worker 只在 localhost 或 HTTPS 下運作。
