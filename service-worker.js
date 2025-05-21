const CACHE_NAME = 'app-cache-v1';
const ASSETS_TO_CACHE = [
  '/', // La raíz si usas index.html
  '/index.html',
  '/test.html',
  // agrega aquí rutas de tus imágenes, estilos y scripts si los tienes
  // por ejemplo:
  // '/styles.css',
  // '/app.js',
  // '/data/content.json'
];

// Instalar y cachear los recursos iniciales
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Activar y limpiar caches viejos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
});

// Interceptar solicitudes y responder desde caché si es posible
self.addEventListener('fetch', (event) => {
  const request = event.request;

  // Solo para GET
  if (request.method !== 'GET') return;

  event.respondWith(
    caches.match(request).then(cachedResponse => {
      // Si lo tenemos en caché, devuélvelo
      if (cachedResponse) {
        // Además, en segundo plano, actualiza
        fetch(request).then(response =>
          caches.open(CACHE_NAME).then(cache => {
            cache.put(request, response.clone());
          })
        ).catch(() => {});
        return cachedResponse;
      }

      // Si no está cacheado, tráelo de la red
      return fetch(request).then(networkResponse => {
        return caches.open(CACHE_NAME).then(cache => {
          cache.put(request, networkResponse.clone());
          return networkResponse;
        });
      });
    }).catch(() => {
      // En caso de fallo total (offline sin caché), podrías servir una imagen fallback
      if (request.destination === 'image') {
        return caches.match('/fallback-image.jpg'); // si la defines
      }
      return new Response('Offline', { status: 503 });
    })
  );
});
