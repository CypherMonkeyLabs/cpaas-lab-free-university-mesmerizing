/* Scope is the directory that contains this file.
   Pages register it with { scope: "./" } resolved from the lab root. */
const CACHE_NAME = "cpaas-lab-v3";
const CACHE_BUDGET_NOTE = "Precache stays under 3.5 MB: shell, chat, one lesson, icons.";
const SHELL_ASSETS = [
  "./",
  "./index.html",
  "./offline.html",
  "./start.html",
  "./play.html",
  "./rooms/sip-jobs.html",
  "./manifest.webmanifest",
  "./favicon.svg",
  "./assets/data/cpaasbot-index.json",
  "./assets/data/catalog.json",
  "./shared/pybot-chat/engine.js",
  "./shared/pybot-chat/ui.js",
  "./shared/pybot-chat/chat.css",
  "./guide/guide.js",
  "./guide/guide.css",
  "./guide/dragbot.js",
  "./guide/cpaas-chat.js",
  "./assets/js/frame.js",
  "./assets/js/university.js",
  "./assets/js/pwa.js",
  "./assets/css/studio.css",
  "./assets/icon-192.png",
  "./assets/icon-512.png",
  "./assets/icon-maskable-512.png",
  "./assets/css/canon.css",
  "./assets/css/cpaas.css",
  "./assets/css/footer.css",
  "./assets/css/frame.css",
  "./assets/css/polish.css",
  "./assets/css/shell.css",
  "./assets/css/uc.css",
  "./assets/css/university.css",
  "./assets/css/wow.css",
  "./assets/fonts/outfit-latin.woff2",
];

self.addEventListener("install", (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => Promise.all(SHELL_ASSETS.map((url) => cache.add(url).catch(() => null))))
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  event.respondWith(
    fetch(req)
      .then((res) => {
        if (res && res.status === 200 && res.type === "basic") {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone)).catch(() => {});
        }
        return res;
      })
      .catch(() => caches.match(req).then((cached) => {
        if (cached) return cached;
        if (req.mode === "navigate") return caches.match("./offline.html");
        return caches.match("./offline.html");
      }))
  );
});
