// Sentra service worker v3 · HTML network-first · css/js stale-while-revalidate · audio/fonts/images cache-on-demand
const V = 'sentra-v3', MEDIA = 'sentra-media-v1';
const SHELL = ['./', 'index.html', 'css/styles.css?v=3', 'js/app.js?v=3', 'js/data.js?v=3', 'js/audio.js?v=3', 'js/install.js?v=3', 'manifest.webmanifest',
  'fonts/Vazirmatn-Regular.woff2', 'fonts/Vazirmatn-Bold.woff2', 'fonts/Vazirmatn-Black.woff2', 'fonts/Fredoka-Bold.woff2',
  'icons/icon-192.png', 'icons/icon-512.png', 'images/shir-o-khorshid.svg', 'images/us.svg'];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys()
  .then(ks => Promise.all(ks.filter(k => k.startsWith('sentra-') && k !== V && k !== MEDIA).map(k => caches.delete(k))))
  .then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  if (/\/(audio|images|fonts|icons)\//.test(url.pathname)) {
    e.respondWith(caches.match(url.origin + url.pathname).then(hit => hit || fetch(req).then(r => { if (r.ok && r.status === 200) { const cp = r.clone(); caches.open(MEDIA).then(c => c.put(url.origin + url.pathname, cp)); } return r; })));
  } else if (req.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('.html')) {
    e.respondWith(fetch(req).then(r => { if (r.ok) { const cp = r.clone(); caches.open(V).then(c => c.put(req, cp)); } return r; })
      .catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match('index.html'))));
  } else {
    e.respondWith(caches.match(req).then(hit => { const net = fetch(req).then(r => { if (r.ok) { const cp = r.clone(); caches.open(V).then(c => c.put(req, cp)); } return r; }).catch(() => hit); return hit || net; }));
  }
});
