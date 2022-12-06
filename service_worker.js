const staticDevCoffee = "Nothing2wear"
const assets = [
  "index.html",
  "api_calls.py",
  "genetic_algorithm.py",
  "vestiti.py",
  "main.py"
]


this.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticDevCoffee).then(cache => {
      cache.addAll(assets)
    })
  )
})

this.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
      caches.match(fetchEvent.request).then(res => {
        return res || fetch(fetchEvent.request)
      })
    )
  })