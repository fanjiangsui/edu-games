/* 由 build_all.py 產生，請勿手改 */
const VERSION = "edu-games-af293e88f8";
const PRECACHE = [
  "./",
  "chinese-idiom/",
  "chinese-idiom/index.html",
  "chinese-idiom/tts-check.html",
  "chinese-idom/",
  "chinese-idom/index.html",
  "chinese-idom/tts-check.html",
  "games.json",
  "icons/apple-touch-icon.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "index.html",
  "manifest.json",
  "mental-models/",
  "mental-models/index.html"
];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(PRECACHE.map(u => new URL(u, self.registration.scope).href))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("edu-games-") && k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, { ignoreSearch: true }).then(hit => hit || fetch(e.request)));
});
