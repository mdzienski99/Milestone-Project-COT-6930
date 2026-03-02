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

Endpoints:

/healthz

/recommend/{user_id}

/metrics

Milestones

M1: Contract + proposal + architecture

M2–M5: Kafka ingest, deployment, evaluation, monitoring, A/B testing, retraining


---

## 7) GitHub “repo hygiene” tasks (do these on GitHub.com)

### A) Create Labels
Repo → **Issues → Labels → New label**
Create:
- `milestone-1`, `milestone-2`, `milestone-3`, `milestone-4`, `milestone-5`
- `kafka`, `ml`, `devops`, `documentation`, `bug`, `enhancement`

### B) Create Project board
Repo → **Projects → New Project → Board**
Columns:
- Backlog
- In Progress
- Done

Create 5–8 issues and add them to the board.

---

## 8) Commit + push your changes

Back in VS Code terminal:

```bash
git status
git add .
git commit -m "Milestone 1: repo skeleton + starter FastAPI + docs"
git push