#!/usr/bin/env python3
"""打包所有遊戲到 docs/（GitHub Pages 發佈這個資料夾）
用法：python3 build_all.py

每個遊戲是 games/<資料夾>/，必須有 game.json（標題、說明等），再選一種打包方式：
  A. 有 build_game.py：執行 `python3 build_game.py <輸出資料夾>`，由它產生 index.html 等檔案
     （適合需要合併、檢查資料的遊戲，例如成語小達人）
  B. 沒有 build_game.py、只有 index.html：直接複製 index.html；有 assets/ 也一起複製
     （適合單一 HTML 檔就能玩的遊戲）
game.json 的 "status" 設成 "草稿" 時不打包、不放上首頁。
任何一個遊戲打包失敗，整個流程就停下來，不會產生不完整的網站。"""
import json, shutil, subprocess, sys, html
from pathlib import Path

root = Path(__file__).parent
docs = root / "docs"
games = []
for g in sorted((root / "games").iterdir()):
    cfg = g / "game.json"
    if not g.is_dir() or not cfg.exists():
        continue
    meta = json.loads(cfg.read_text(encoding="utf-8")); meta["slug"] = g.name
    if meta.get("status") == "草稿":
        print(f"[{g.name}] 草稿，略過"); continue
    out = docs / g.name; out.mkdir(parents=True, exist_ok=True)
    if (g / "build_game.py").exists():
        r = subprocess.run([sys.executable, "build_game.py", str(out)], cwd=g)
        if r.returncode != 0:
            sys.exit(f"[{g.name}] 打包失敗，停止")
    elif (g / "index.html").exists():
        shutil.copy2(g / "index.html", out / "index.html")
        if (g / "assets").is_dir():
            shutil.copytree(g / "assets", out / "assets", dirs_exist_ok=True)
    else:
        sys.exit(f"[{g.name}] 找不到 build_game.py 或 index.html，不知道怎麼打包")
    if not (out / "index.html").exists():
        sys.exit(f"[{g.name}] 打包後沒有產生 index.html，停止")
    print(f"[{g.name}] 完成")
    games.append(meta)

cards = "\n".join(
    f'''    <a class="game" href="{html.escape(m['slug'])}/">
      <b>{html.escape(m['title'])}</b>
      <span>{html.escape(m.get('description', ''))}</span>
      <small>{html.escape(m.get('audience', ''))}・{html.escape(m.get('note', ''))}</small>
    </a>''' for m in games)
(docs / "index.html").write_text(f'''<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>學習小遊戲</title>
<style>
:root {{ --bg:#fbf7f0; --card:#fff; --ink:#2b2420; --muted:#7a6e64; --line:#e8dfd3; --accent:#c0392b; --accent-soft:#fbe9e6; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#1d1916; --card:#2a2420; --ink:#f2ebe3; --muted:#b3a597; --line:#3d342d; --accent:#e8735f; --accent-soft:#3d2622; color-scheme: dark; }} }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif; line-height:1.6; }}
main {{ max-width:640px; margin:0 auto; padding-inline:16px; padding-block:32px 48px; }}
h1 {{ color:var(--accent); letter-spacing:2px; margin:0 0 4px; }}
p {{ color:var(--muted); margin:0 0 20px; }}
.list {{ display:grid; gap:12px; }}
.game {{ display:grid; gap:4px; padding:16px; border:1.5px solid var(--line); border-radius:14px; background:var(--card); color:inherit; text-decoration:none;
  transition: transform .12s, border-color .12s, background-color .12s, box-shadow .12s; }}
.game b {{ font-size:20px; }}
.game small {{ color:var(--muted); }}
.game:hover {{ transform:translateY(-3px); border-color:var(--accent); background:var(--accent-soft); box-shadow:0 6px 16px rgba(0,0,0,.12); }}
.game:focus-visible {{ outline:3px solid var(--accent); outline-offset:2px; }}
footer {{ margin-top:24px; font-size:14px; color:var(--muted); }}
</style>
</head>
<body>
<main>
  <h1>學習小遊戲</h1>
  <p>給孩子玩的離線學習遊戲，用手機或電腦的瀏覽器打開就能玩。</p>
  <div class="list">
{cards}
  </div>
  <footer>內容由 AI 協助整理，可能有誤；發現錯誤歡迎回報。</footer>
</main>
</body>
</html>
''', encoding="utf-8")
(docs / ".nojekyll").write_text("")
print(f"完成：{len(games)} 個遊戲 → docs/")
