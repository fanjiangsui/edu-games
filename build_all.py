#!/usr/bin/env python3
"""打包所有遊戲到 docs/（GitHub Pages 發佈這個資料夾）
用法：python3 build_all.py

每個遊戲是 games/<資料夾>/，必須有 game.json（標題、說明等），再選一種打包方式：
  A. 有 build_game.py：執行 `python3 build_game.py <輸出資料夾>`，由它產生 index.html 等檔案
     （適合需要合併、檢查資料的遊戲，例如成語小達人）
  B. 沒有 build_game.py、只有 index.html：直接複製 index.html；有 assets/ 也一起複製
     （適合單一 HTML 檔就能玩的遊戲）
game.json 可加 "icon"（一個 emoji，顯示在首頁卡片）。
game.json 的 "status" 設成 "草稿" 時不打包、不放上首頁。
任何一個遊戲打包失敗，整個流程就停下來，不會產生不完整的網站。"""
import hashlib, json, shutil, subprocess, sys
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

# 在每個遊戲頁加上 manifest 連結與離線註冊（只改打包結果，不動遊戲原始檔；重複執行不會重複加）
MARK = "<!--hub-pwa-->"
HEAD_ADD = (MARK + '<link rel="manifest" href="../manifest.json"><link rel="apple-touch-icon" href="../icons/apple-touch-icon.png">'
            '<style>#hub-home{position:fixed;z-index:2147483647;left:max(8px,env(safe-area-inset-left));top:max(8px,env(safe-area-inset-top));'
            'padding:6px 12px;border-radius:999px;background:rgba(43,36,32,.78);color:#fff;font:600 14px/1.4 system-ui,"PingFang TC","Microsoft JhengHei",sans-serif;'
            'text-decoration:none;box-shadow:0 1px 6px rgba(0,0,0,.3)}#hub-home:focus-visible{outline:3px solid #fff;outline-offset:2px}</style>')
BODY_ADD = ('<a id="hub-home" href="../" aria-label="回到首頁">← 首頁</a><script>if("serviceWorker"in navigator)addEventListener("load",function(){'
            'navigator.serviceWorker.register("../sw.js",{scope:"../",updateViaCache:"none"}).catch(function(){})})</script>')
def inject(f):
    t = f.read_text(encoding="utf-8")
    if MARK in t:
        return
    h, b = t.rfind("</head>"), t.rfind("</body>")
    t = t[:h] + HEAD_ADD + t[h:] if h >= 0 else HEAD_ADD + t
    b = t.rfind("</body>")
    t = t[:b] + BODY_ADD + t[b:] if b >= 0 else t + BODY_ADD
    f.write_text(t, encoding="utf-8")
for m in games:
    for f in (docs / m["slug"]).glob("*.html"):
        inject(f)

# 首頁、圖示、games.json、manifest
shutil.copy2(root / "hub" / "index.html", docs / "index.html")
shutil.copytree(root / "hub" / "icons", docs / "icons", dirs_exist_ok=True)
listing = [{"name": m["title"], "description": m.get("description", ""), "path": m["slug"] + "/",
            "icon": m.get("icon", ""), "audience": m.get("audience", ""), "note": m.get("note", "")} for m in games]
(docs / "games.json").write_text(json.dumps(listing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(docs / "manifest.json").write_text(json.dumps({
    "name": "學習小遊戲", "short_name": "學習小遊戲", "description": "給孩子與大人的離線學習小遊戲",
    "start_url": "./", "scope": "./", "display": "standalone", "lang": "zh-Hant-TW",
    "background_color": "#fbf7f0", "theme_color": "#c0392b",
    "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
              {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]},
    ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(docs / ".nojekyll").write_text("")

# sw.js：預先快取 docs/ 裡所有檔案；版本號 = 檔案內容雜湊，內容一變就換新快取、清掉舊的
files = sorted(f for f in docs.rglob("*") if f.is_file() and f.name not in ("sw.js", ".nojekyll"))
ver = hashlib.sha1(b"".join(f.relative_to(docs).as_posix().encode() + f.read_bytes() for f in files)).hexdigest()[:10]
urls = ["./"] + [f.relative_to(docs).as_posix() for f in files]
urls += [u[:-len("index.html")] for u in urls if u.endswith("/index.html")]
(docs / "sw.js").write_text(f"""/* 由 build_all.py 產生，請勿手改 */
const VERSION = "edu-games-{ver}";
const PRECACHE = {json.dumps(sorted(set(urls)), ensure_ascii=False, indent=2)};
self.addEventListener("install", e => {{
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(PRECACHE.map(u => new URL(u, self.registration.scope).href))).then(() => self.skipWaiting()));
}});
self.addEventListener("activate", e => {{
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("edu-games-") && k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
}});
self.addEventListener("fetch", e => {{
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, {{ ignoreSearch: true }}).then(hit => hit || fetch(e.request)));
}});
""", encoding="utf-8")
print(f"完成：{len(games)} 個遊戲 → docs/（快取版本 edu-games-{ver}）")
