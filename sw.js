const CACHE='urna-educativa-shell-v4';
const SHELL=['./mobile-v4.html','./offline-app.js','./manifest.webmanifest','./admin-v4.html'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET') return;
  if(u.origin===location.origin){
    e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request).then(r=>{const clone=r.clone();caches.open(CACHE).then(c=>c.put(e.request,clone));return r;}).catch(()=>caches.match('./mobile-v4.html'))));
  }
});
