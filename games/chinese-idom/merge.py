#!/usr/bin/env python3
"""合併範例資料與各批次資料：python3 merge.py → data/idioms.json"""
import json
from pathlib import Path

here = Path(__file__).parent
files = [here / "idioms.sample.json"] + sorted((here / "data/batches").glob("batch-[0-9][0-9].json"))
items, seen = [], set()
for f in files:
    for it in json.loads(f.read_text(encoding="utf-8"))["items"]:
        if it["id"] in seen:
            raise SystemExit(f"重複的 id：{it['id']}（{f.name}）")
        seen.add(it["id"]); items.append(it)
items.sort(key=lambda it: it["id"])
# 朗讀覆寫：手機語音念錯的成語，改用同音字朗讀
tts_path = here / "data/tts-overrides.json"
if tts_path.exists():
    tts = {k: v for k, v in json.loads(tts_path.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    ids = {it["id"] for it in items}
    unknown = set(tts) - ids
    if unknown: raise SystemExit(f"tts-overrides 有不存在的 id：{sorted(unknown)}")
    for it in items:
        if it["id"] in tts:
            if len(tts[it["id"]]) != len(it["idiom"]): raise SystemExit(f"{it['id']} 朗讀文字字數不符")
            it["tts"] = tts[it["id"]]
out = here / "data/idioms.json"
out.write_text(json.dumps({"version": "0.2.0", "items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"已合併 {len(files)} 個檔案，共 {len(items)} 個成語 → {out.relative_to(here)}")
