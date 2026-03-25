from fastapi import FastAPI, Query
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from collections import Counter as PyCounter
import pandas as pd
import json
import os

app = FastAPI()

reqs = Counter("recommend_requests_total", "requests", ["status"])
lat = Histogram("recommend_latency_seconds", "latency")

POPULARITY_PATH = "artifacts/popularity.json"
ITEM_CF_PATH = "artifacts/item_cf.json"
SNAPSHOT_PATH = "snapshots/watch_events.csv"


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_user_history(user_id: int):
    if not os.path.exists(SNAPSHOT_PATH):
        return []
    df = pd.read_csv(SNAPSHOT_PATH)
    if "user_id" not in df.columns or "movie_id" not in df.columns:
        return []
    return df[df["user_id"] == user_id]["movie_id"].tolist()


@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": os.getenv("MODEL_VERSION", "m2")}


@app.get("/recommend/{user_id}")
@lat.time()
def recommend(user_id: int, k: int = 10, model: str = Query(default="popularity")):
    try:
        if model == "popularity":
            artifact = load_json(POPULARITY_PATH)
            if not artifact:
                raise FileNotFoundError("popularity.json not found")
            recs = artifact["items"][:k]

        elif model == "item_cf":
            artifact = load_json(ITEM_CF_PATH)
            if not artifact:
                raise FileNotFoundError("item_cf.json not found")

            history = get_user_history(user_id)
            if not history:
                pop = load_json(POPULARITY_PATH)
                recs = pop["items"][:k] if pop else []
            else:
                counts = PyCounter()
                neighbors = artifact["neighbors"]

                for movie_id in history:
                    for related in neighbors.get(str(movie_id), []):
                        if related not in history:
                            counts[related] += 1

                recs = [movie for movie, _ in counts.most_common(k)]

                if not recs:
                    pop = load_json(POPULARITY_PATH)
                    recs = pop["items"][:k] if pop else []

        else:
            raise ValueError("model must be 'popularity' or 'item_cf'")

        reqs.labels("200").inc()
        return {
            "user_id": user_id,
            "model_version": os.getenv("MODEL_VERSION", "m2"),
            "model": model,
            "recommendations": recs
        }

    except Exception as e:
        reqs.labels("500").inc()
        return {"error": str(e)}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)