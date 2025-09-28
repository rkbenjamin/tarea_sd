from flask import Flask, request, jsonify
import time, os
from collections import OrderedDict

app = Flask(__name__)

class Cache:
    def __init__(self, capacity=100, policy="LRU", ttl=1200):
        self.capacity = int(capacity)
        self.policy = policy.upper()
        self.ttl = int(ttl)
        self.store = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self.store:
            value, ts = self.store[key]
            if time.time() - ts < self.ttl:
                self.hits += 1
                if self.policy == "LRU":
                    self.store.move_to_end(key)
                return value
            else:
                del self.store[key]
        self.misses += 1
        return None

    def put(self, key, value):
        now = time.time()
        if key in self.store:
            self.store[key] = (value, now)
            if self.policy == "LRU":
                self.store.move_to_end(key)
        else:
            if len(self.store) >= self.capacity:
                self.store.popitem(last=(self.policy == "LRU"))
            self.store[key] = (value, now)

cache = Cache(
    capacity=os.getenv("CACHE_CAPACITY", 100),
    policy=os.getenv("CACHE_POLICY", "LRU"),
    ttl=os.getenv("CACHE_TTL", 1200)
)

@app.route("/check", methods=["POST"])
def check():
    q = request.json["question"]
    ans = cache.get(q)
    return jsonify({"hit": ans is not None, "answer": ans})

@app.route("/insert", methods=["POST"])
def insert():
    data = request.json
    cache.put(data["question"], data["answer"])
    return jsonify({"status": "ok"})

@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "policy": cache.policy,
        "capacity": cache.capacity,
        "ttl": cache.ttl,
        "items": len(cache.store),
        "hits": cache.hits,
        "misses": cache.misses
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)