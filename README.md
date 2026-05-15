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
pip install psutil prometheus-client requests python-dotenv pyyaml
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


## Check Anomaly Output

```python
python3 -c "import sqlite3; c=sqlite3.connect('monitor.db').cursor(); rows=c.execute('SELECT timestamp, metric_name, value, avarage_value, offender_process FROM anomalies ORDER BY rowid DESC LIMIT 20').fetchall(); [print(r) for r in rows]"
```

## Update Log

- 2026-05-15: README simplified to essentials.
