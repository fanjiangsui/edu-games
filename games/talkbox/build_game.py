#!/usr/bin/env python3
"""話匣子的打包入口（由 build_all.py 呼叫）：python3 build_game.py 輸出資料夾
只複製網頁執行需要的檔案；parts/、build_questions.js、make_icons.py 是製作工具，不放上網站。
題庫要改：編輯 parts/*.txt → node build_questions.js → 調高 sw.js 的 VERSION（見 README.md）。"""
import shutil, sys
from pathlib import Path

here = Path(__file__).parent
out = Path(sys.argv[1]).resolve()
for name in ("index.html", "questions.js", "sw.js", "manifest.webmanifest"):
    if not (here / name).exists():
        sys.exit(f"缺少 {name}，停止打包")
    shutil.copy2(here / name, out / name)
shutil.copytree(here / "icons", out / "icons", dirs_exist_ok=True)
