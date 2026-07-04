const CACHE_NAME = 'lms-pwa-cache-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/accounts/login/',
  '/static/manifest.json',
  '/static/css/styles.css',
  '/static/vendor/bootstrap.min.css',
  '/static/vendor/bootstrap.bundle.min.js',
  '/static/vendor/chart.umd.js',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

// Install Service Worker and cache essential files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Caching Application Shell...');
        // We use allSettled or catch on individual items to avoid entire cache failure if some urls aren't reachable (e.g. '/' requires login)
        return Promise.allSettled(
          ASSETS_TO_CACHE.map(url => {
            return cache.add(url).catch(err => console.warn(`Failed to cache asset: ${url}`, err));
          })
        );
      })
      .then(() => self.skipWaiting())
  );
});

// Activate Service Worker and clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('[Service Worker] Clearing old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch events: Network first, fallback to Cache, then fallback to offline text
self.addEventListener('fetch', event => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // If successful, open cache and clone response
        if (response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Offline: attempt cache match
        return caches.match(event.request).then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // If the resource requested is HTML and not in cache, we could return a simple offline page or message
          if (event.request.headers.get('accept').includes('text/html')) {
            return new Response(
              `<!DOCTYPE html>
              <html lang="en">
              <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Offline | Lead Management System</title>
                <link rel="stylesheet" href="/static/vendor/bootstrap.min.css">
                <link rel="stylesheet" href="/static/css/styles.css">
              </head>
              <body class="bg-light d-flex align-items-center justify-content-center" style="min-height: 100vh;">
                <div class="card p-5 text-center shadow-lg border-0" style="max-width: 500px; border-radius: 16px;">
                  <div class="text-primary mb-3">
                    <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="currentColor" class="bi bi-wifi-off" viewBox="0 0 16 16">
                      <path d="M10.707 11.193a.5.5 0 0 0 .003-.707L8.715 8.49a.5.5 0 0 0-.707.003l-2 2a.5.5 0 0 0 .707.707L8 9.914l1.996 1.986a.5.5 0 0 0 .711-.707z"/>
                      <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM1.49 5.25a6.5 6.5 0 0 0-.3 2.186l1.242 1.242A5.02 5.02 0 0 1 3.5 5.5l-.656-.656A6.477 6.477 0 0 0 1.49 5.25zm1.51-1.51L4.242 5A4.975 4.975 0 0 1 8 3.5c1.378 0 2.628.56 3.535 1.464l1.242 1.242a6.5 6.5 0 0 0-9.777-2.464z"/>
                    </svg>
                  </div>
                  <h3 class="fw-bold">You are Offline</h3>
                  <p class="text-muted">It seems you don't have an active internet connection. Some views and actions might be unavailable.</p>
                  <a href="/" class="btn btn-primary btn-primary-custom w-100 mt-3">Try Reconnecting</a>
                </div>
              </body>
              </html>`,
              {
                headers: { 'Content-Type': 'text/html' }
              }
            );
          }
        });
      })
  );
});
