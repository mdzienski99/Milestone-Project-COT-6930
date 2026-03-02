# Milestone-Project-COT-6930
Welcome to the repo of this project. 
# Real-Time Movie Recommender (ML & AI in Production)
 
Members: **Michal Dzienski, Rayan Rabbi**

## Overview
This project builds a real-time movie recommendation system using MovieLens data + Kafka event streaming.
A FastAPI service serves recommendations and emits events for online evaluation (success within N minutes).

## Architecture
See the Milestone 1 PDF for the full architecture diagram.
Key components:
- FastAPI on Cloud Run
- Kafka (Confluent Cloud) topics: `team.watch_events`, `team.reco_responses`, `team.rate_events`
- ETL consumer writing Parquet to object storage
- Training pipeline + model registry
- CI/CD via GitHub Actions → GHCR → deploy to Cloud Run
- Monitoring via Prometheus `/metrics` + Grafana

## Local Run (starter)
```bash
python -m venv .venv
# activate venv...
pip install -r requirements.txt
uvicorn service.app:app --reload --port 8000