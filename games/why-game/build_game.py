#!/usr/bin/env python3
"""十萬個為什麼的打包入口（由 build_all.py 呼叫）：python3 build_game.py 輸出資料夾
只複製網頁執行需要的檔案；parts/、build_questions.js 是製作工具，不放上網站。
題庫要改：編輯 parts/*.txt → node build_questions.js（會檢查格式與選項長度偏差）→ 再打包。"""
import shutil, sys
from pathlib import Path

here = Path(__file__).parent
out = Path(sys.argv[1]).resolve()
for name in ("index.html", "questions.js"):
    if not (here / name).exists():
        sys.exit(f"缺少 {name}，停止打包（題庫要先跑 node build_questions.js）")
    shutil.copy2(here / name, out / name)
