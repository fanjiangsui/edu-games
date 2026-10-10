#!/usr/bin/env python3
"""把成語資料嵌進遊戲模板，產生單一離線 HTML：python3 build.py [資料.json] [輸出.html]"""
import json, sys
from pathlib import Path

here = Path(__file__).parent
default_data = here / "data/idioms.json" if (here / "data/idioms.json").exists() else here / "idioms.sample.json"
data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_data
out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "成語小達人.html"

data = json.loads(data_path.read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
tpl = (here / "game.template.html").read_text(encoding="utf-8")
assert tpl.count("/*__DATA__*/null") == 1, "模板中找不到資料佔位符"
out_path.write_text(tpl.replace("/*__DATA__*/null", payload), encoding="utf-8")
print(f"已產生 {out_path.name}（{len(data['items'])} 個成語，{out_path.stat().st_size // 1024} KB）")
