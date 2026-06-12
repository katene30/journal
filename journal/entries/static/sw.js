// Basic service worker for PWA installability
const CACHE_NAME = 'journal-v1';

// Install event - cache basic assets
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});

// Fetch event - network first, no offline fallback for now
self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request));
});
