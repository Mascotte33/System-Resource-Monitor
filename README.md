# System Resource Monitor

Monitors CPU, RAM, and disk usage, calculates a health score, detects anomalies, stores them in SQLite, and exposes Prometheus metrics for Grafana.

## Tech Stack

- Python 3.10+
- SQLite
- Docker Compose
- Prometheus
- Grafana

## Quick Start

1. Create and activate environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env`:

```env
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

4. Start observability stack:

```bash
docker compose up -d
```

5. Run monitor:

```bash
python3 main.py
```

## Run Tests

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Test Anomalies

Install stress tool:

```bash
sudo apt install stress
```

Trigger Tests:

```bash
stress --cpu 4 --timeout 25
stress --vm 1 --vm-bytes 80% --timeout 25
stress --hdd 1 --hdd-bytes 2G --timeout 25
```

## Check Anomaly Output

```bash
python3 -c "import sqlite3; c=sqlite3.connect('monitor.db').cursor(); rows=c.execute('SELECT timestamp, metric_name, value, avarage_value, offender_process FROM anomalies ORDER BY rowid DESC LIMIT 20').fetchall(); [print(r) for r in rows]"
```

## Project Structure

- `main.py` — orchestration loop
- `config/config.yaml` — all thresholds, weights, and settings
- `config/logger_config.py` — shared logging setup
- `collector/metrics.py` — psutil metric collection
- `health/score.py` — weighted health score (0-100)
- `anomaly/detector.py` — spike detection against rolling baseline
- `db/storage.py` — SQLite baseline and anomaly persistence
- `alerts/discord.py` — Discord webhook alerts with retry
- `exporter.py` — Prometheus metrics endpoint (port 8000)
- `tests/test_core.py` — unit tests for core logic

## Update Log

- 2026-05-19: Added structured logging, Discord retry/backoff, baseline pruning, anomaly log lines, unit tests.
- 2026-05-15: Initial project setup with Prometheus/Grafana stack.
