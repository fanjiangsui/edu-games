#!/usr/bin/env python3
"""成語小達人的打包入口（由 build_all.py 呼叫）：python3 build_game.py 輸出資料夾
步驟：合併資料 → 檢查（有錯就停）→ 產生遊戲 index.html → 產生朗讀檢查頁 tts-check.html"""
import subprocess, sys
from pathlib import Path

here = Path(__file__).parent
out = Path(sys.argv[1]).resolve()
run = lambda *a: subprocess.run([sys.executable, *a], cwd=here, check=True)

run("merge.py")
r = subprocess.run([sys.executable, "validate.py", "data/idioms.json", "--list", "list/idiom-list-500.json"],
                   cwd=here, capture_output=True, text=True)
lines = r.stdout.strip().splitlines()
print(lines[-1] if lines else r.stderr.strip())
if r.returncode != 0:
    print(r.stdout, r.stderr)
    sys.exit("資料檢查有錯誤，停止打包")
run("build.py", "data/idioms.json", str(out / "index.html"))
run("build_tts_check.py", "data/idioms.json", str(out / "tts-check.html"))
