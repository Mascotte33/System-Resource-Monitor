import datetime
import sqlite3


def init_db() -> None:
    connection = sqlite3.connect("monitor.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS baselines("
    "timestamp TEXT,"         \
    "metric_name TEXT," \
    "value  REAL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS anomalies("
    "timestamp TEXT,"                    \
    "metric_name TEXT, " \
    "value REAL, " \
    "avarage_value REAL," \
    "offender_process TEXT)")

    connection.commit()
    connection.close()

def add_baseline(metric_name : str, value : float) -> None:
    timestamp = datetime.datetime.now().strftime("%d-%m-%YT%H:%M:%SZ")
    connection = sqlite3.connect("monitor.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO baselines VALUES (?, ?, ?)", (timestamp, metric_name, value))
    connection.commit()
    connection.close()

def get_baseline_avarage(metric_name : str, window : float) -> float:
    connection = sqlite3.connect("monitor.db")
    cursor = connection.cursor()
    cursor.execute("SELECT AVG(value) FROM baselines \
                   WHERE metric_name = ? \
                   ORDER BY timestamp DESC \
                   LIMIT ?", (metric_name, window) )
    baseline_avarage = cursor.fetchone()
    connection.close()
    
    return baseline_avarage[0] if baseline_avarage[0] is not None else 0.0

def add_anomalies(metric_name : str, value : float, offender_process : dict, config : dict) -> None:
    timestamp = datetime.datetime.now().strftime("%d-%m-%YT%H:%M:%SZ")
    avarage_value = get_baseline_avarage(metric_name, config['collection']['baseline_window'])

    connection = sqlite3.connect("monitor.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO anomalies VALUES (?, ?, ?, ?, ?)",(timestamp, metric_name, value, avarage_value, offender_process))
    connection.commit()
    connection.close()
