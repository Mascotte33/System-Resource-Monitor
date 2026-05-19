import psutil

def collect_metrics() -> dict:

    processes = []
    for proc in psutil.process_iter(['pid','name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            processes.append({
                'pid': info['pid'],
                'name' : info['name'],
                'cpu_percent' : info['cpu_percent'],
                'memory_percent' : info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    top_procesess = sorted(
        processes,
        key=lambda p: p['memory_percent'],
        reverse=True
    )
    
    metrics = {
        "cpu_percent" : psutil.cpu_percent(interval=1),
        "ram_percent" : psutil.virtual_memory().percent,
        "disk_percent" : psutil.disk_usage('/').percent,
       # "temp_celsius" : psutil.sensors_temperatures(),         -To add when on real machine because WSL does not show temps
        "top_ten_processes" : top_procesess[:10]
    }

    return metrics
