#!/usr/bin/env python3
"""產生破音字朗讀檢查頁：python3 build_tts_check.py 資料.json 輸出.html"""
import json, sys
from pathlib import Path
here = Path(__file__).parent
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["items"]
sub = [{"id": i["id"], "w": i["idiom"], "z": i["zhuyin"],
        "p": [[x["char"], x["here"], x["other"]] for x in i.get("polyphones", [])], "t": i.get("tts")}
       for i in data if i.get("polyphones") or i.get("tts")]
body = (here / "tts-check.template.html").read_text(encoding="utf-8").replace(
    "/*__DATA__*/[]", json.dumps(sub, ensure_ascii=False, separators=(",", ":")))
head, rest = body.split('<div class="wrap">', 1)
Path(sys.argv[2]).write_text(
    '<!doctype html>\n<html lang="zh-Hant-TW">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + head + '</head>\n<body>\n<div class="wrap">' + rest + '\n</body>\n</html>\n', encoding="utf-8")
print(f"已產生 {Path(sys.argv[2]).name}（{len(sub)} 個成語）")
