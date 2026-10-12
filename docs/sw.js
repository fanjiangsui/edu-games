/* 由 build_all.py 產生，請勿手改 */
const VERSION = "edu-games-00a05dc399";
const PRECACHE = [
  "./",
  "chinese-idiom/",
  "chinese-idiom/favicon.svg",
  "chinese-idiom/index.html",
  "chinese-idiom/tts-check.html",
  "chinese-idom/",
  "chinese-idom/index.html",
  "chinese-idom/tts-check.html",
  "favicon.svg",
  "games.json",
  "icons/apple-touch-icon.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "index.html",
  "manifest.json",
  "mental-models/",
  "mental-models/favicon.svg",
  "mental-models/index.html",
  "watermelon-darts/",
  "watermelon-darts/index.html"
];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(PRECACHE.map(u => new URL(u, self.registration.scope).href))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("edu-games-") && k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  const scope = new URL(self.registration.scope);
  const top = url.origin === scope.origin && (url.pathname === scope.pathname || url.pathname === scope.pathname + "index.html" || url.pathname === scope.pathname + "games.json");
  if (top) {
    // 首頁與遊戲清單：先抓最新（新增遊戲馬上看得到），沒網路才用快取
    e.respondWith(fetch(e.request, { cache: "no-cache" }).then(r => {
      const copy = r.clone();
      caches.open(VERSION).then(c => c.put(e.request, copy));
      return r;
    }).catch(() => caches.match(e.request, { ignoreSearch: true })));
    return;
  }
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request)));
});
