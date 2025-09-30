from flask import Flask, jsonify, request
import requests, os, time

app = Flask(__name__)

ALMACENAMIENTO_URL = os.getenv("ALMACENAMIENTO_URL", "http://almacenamiento:5004")
CACHE_URL   = os.getenv("CACHE_URL", "http://cache:5001")
LLM_URL     = os.getenv("LLM_URL", "http://llm:5002")
PUNTAJE_URL   = os.getenv("PUNTAJE_URL", "http://puntaje:5003")

DEFAULT_DIST   = os.getenv("TRAFFIC_DIST", "uniform")
ZIPF_ALPHA     = os.getenv("ZIPF_ALPHA", "1.2")
POISSON_LAMBDA = os.getenv("POISSON_LAMBDA", "10")

@app.route("/consulta", methods=["GET"])
def consulta():
    dist  = request.args.get("dist", DEFAULT_DIST).lower()
    alpha = request.args.get("alpha", ZIPF_ALPHA)
    lam   = request.args.get("lambda", POISSON_LAMBDA)

    params = {"dist": dist}
    if dist == "zipf":
        params["alpha"] = alpha
    elif dist == "poisson":
        params["lambda"] = lam

    r = requests.get(f"{ALMACENAMIENTO_URL}/random", params=params)
    data = r.json()
    if not data.get("ok"):
        return jsonify({"error": "sin datos en almacenamiento", "details": data}), 500

    qrow = data["data"]
    q = qrow["title"]
    human_a = qrow["best_answer"]

    resp = requests.post(f"{CACHE_URL}/check", json={"question": q})
    cj = resp.json()
    if cj["hit"]:
        llm_a = cj["answer"]
    else:
        t0 = time.time()
        llm_resp = requests.post(f"{LLM_URL}/answer", json={"question": q})
        t1 = time.time()
        llm_a = llm_resp.json()["answer"]
        llm_latency_ms = int((t1 - t0) * 1000)
        requests.post(f"{CACHE_URL}/insert", json={"question": q, "answer": llm_a})

    score_resp = requests.post(f"{PUNTAJE_URL}/compute",
                               json={"human_answer": human_a, "llm_answer": llm_a})
    score = score_resp.json()["puntaje"]

    requests.post(f"{ALMACENAMIENTO_URL}/save",
                  json={"question": q, "human_answer": human_a,
                        "llm_answer": llm_a, "score": score})

    return jsonify({
        "question": q,
        "human_answer": human_a,
        "llm_answer": llm_a,
        "score": score,
        "dist": dist,
        "alpha": alpha
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)