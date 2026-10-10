#!/usr/bin/env python3
"""成語資料檢查
用法：python3 validate.py 資料.json [schema.json] [--list list/idiom-list-500.json]
--list：提供 500 成語清單時，會額外檢查 id／成語／難度和清單一致、填空選項都在清單內"""
import json, re, sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    jsonschema = None

ZHUYIN_RE = re.compile(r"^[ㄅ-ㄩ]+[ˊˇˋ˙]?$|^˙[ㄅ-ㄩ]+$")


def main():
    args = sys.argv[1:]
    list_path = None
    if "--list" in args:
        i = args.index("--list"); list_path = Path(args[i + 1]); del args[i:i + 2]
    here = Path(__file__).parent
    data_path = Path(args[0] if args else "idioms.sample.json")
    schema_path = Path(args[1] if len(args) > 1 else here / "schema.json")
    data = json.loads(data_path.read_text(encoding="utf-8"))
    errors, warnings = [], []

    if jsonschema:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        v = jsonschema.Draft202012Validator(schema)
        for e in v.iter_errors(data):
            errors.append(f"[schema] {'/'.join(map(str, e.path))}: {e.message}")
    else:
        warnings.append("未安裝 jsonschema，略過 schema 檢查（pip install jsonschema）")

    items = data.get("items", [])
    all_idioms = {it["idiom"] for it in items}
    listed = None
    if list_path:
        listed = {x["idiom"]: x for x in json.loads(list_path.read_text(encoding="utf-8"))["items"]}
        all_idioms |= set(listed)
    seen_id, seen_idiom = set(), set()

    for it in items:
        tag = f"{it.get('id')} {it.get('idiom')}"
        if it["id"] in seen_id: errors.append(f"{tag}: id 重複")
        if it["idiom"] in seen_idiom: errors.append(f"{tag}: 成語重複")
        seen_id.add(it["id"]); seen_idiom.add(it["idiom"])

        if listed is not None:
            ref = listed.get(it["idiom"])
            if not ref: errors.append(f"{tag}: 不在 500 成語清單中")
            elif ref["id"] != it["id"] or ref["level"] != it["level"]:
                errors.append(f"{tag}: id 或難度與清單不符（清單：{ref['id']}、{ref['level']}）")
        if it["origin"]["source"] is None and it["origin"]["quote"]:
            errors.append(f"{tag}: 沒有出處卻有原文摘句")
        if len(it["zhuyin"]) != len(it["idiom"]):
            errors.append(f"{tag}: 注音數 {len(it['zhuyin'])} ≠ 字數 {len(it['idiom'])}")
        for z in it["zhuyin"]:
            if not ZHUYIN_RE.match(z):
                errors.append(f"{tag}: 注音格式怪異「{z}」")

        for p in it.get("polyphones", []):
            if p["char"] not in it["idiom"]:
                errors.append(f"{tag}: 破音字「{p['char']}」不在成語中")
            else:
                idx = it["idiom"].index(p["char"])
                if it["zhuyin"][idx] != p["here"]:
                    errors.append(f"{tag}: 破音字「{p['char']}」讀音與 zhuyin 不一致")

        for k in it["key_chars"]:
            if k["char"] not in it["idiom"]:
                errors.append(f"{tag}: key_chars「{k['char']}」不在成語中")

        q = it["quiz"]
        for name in ("meaning_mcq", "fill_blank"):
            m = q[name]
            if not 0 <= m["answer_index"] < len(m["choices"]):
                errors.append(f"{tag}: {name} answer_index 超出範圍")
            if len(set(m["choices"])) != len(m["choices"]):
                errors.append(f"{tag}: {name} 選項重複")
        fb = q["fill_blank"]
        if "＿＿" not in fb["sentence"]:
            errors.append(f"{tag}: fill_blank 句子缺少「＿＿」")
        if fb["choices"][fb["answer_index"]] != it["idiom"]:
            errors.append(f"{tag}: fill_blank 正解不是本成語")
        for c in fb["choices"]:
            if c not in all_idioms:
                (errors if listed is not None else warnings).append(f"{tag}: 填空選項「{c}」不在成語清單中")

        if not any(it["idiom"] in s for s in it["examples"]):
            errors.append(f"{tag}: 例句中沒有出現成語")
        if it["review"]["status"] == "draft":
            warnings.append(f"{tag}: 尚未人工校對")

    for e in errors: print("ERROR  ", e)
    for w in warnings: print("WARN   ", w)
    print(f"\n共 {len(items)} 筆，{len(errors)} 個錯誤，{len(warnings)} 個提醒")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
