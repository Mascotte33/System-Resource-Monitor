import socket

from prometheus_client import Gauge, Counter, start_http_server

cpu_percent = Gauge(
    "cpu_percent",
    'Percentage of the CPU usage',
    ['hostname']
)

ram_percent = Gauge(
    'ram_percent',
    'Percentage of the RAM usage',
    ['hostname']
)

disk_percent = Gauge(
    'disk_percent',
    'Percentage of the DISK usage',
    ['hostname']
)

health_score = Gauge(
    'health_score',
    'Health score of the system from 0-100',
    ['hostname']
) 

anomalies_counter = Counter(
    'anomalies_counter',
    'Total number of anomalies that occured',
    ['hostname', 'metric_name'],
    
)


def start_exporter(port : int) -> None:
    start_http_server(port)

def update_metrics(metrics_dict : dict, score : float) -> None:
    hostname = socket.gethostname()

    cpu_percent.labels(hostname).set(metrics_dict['cpu_percent'])
    ram_percent.labels(hostname).set(metrics_dict['ram_percent'])
    disk_percent.labels(hostname).set(metrics_dict['disk_percent'])
    health_score.labels(hostname).set(score)

def increment_anomaly_counter(metrics_name:str) -> None:
    hostname = socket.gethostname()
    anomalies_counter.labels(hostname, metric_name=metrics_name).inc()

