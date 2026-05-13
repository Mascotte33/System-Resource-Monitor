from prometheus_client import Gauge, Counter, start_http_server

cpu_percent = Gauge(
    "cpu_percent",
    'Percentage of the CPU usage'
)

ram_percent = Gauge(
    'ram_percent',
    'Percentage of the RAM usage'
)

disk_percent = Gauge(
    'disk_percent',
    'Percentage of the DISK usage'
)

health_score = Gauge(
    'health_score',
    'Health score of the system from 0-100'
) 

anomalies_counter = Counter(
    'anomalies_counter',
    'Total number of anomalies that occured',
    ['metric_name']
)


def start_exporter(port : int) -> None:
    start_http_server(port)

def update_metrics(metrics_dict : dict, score : float) -> None:
    cpu_percent.set(metrics_dict['cpu_percent'])
    ram_percent.set(metrics_dict['ram_percent'])
    disk_percent.set(metrics_dict['disk_percent'])
    health_score.set(score)

def increment_anomaly_counter(metrics_name:str) -> None:
    anomalies_counter.labels(metrics_name).inc()

