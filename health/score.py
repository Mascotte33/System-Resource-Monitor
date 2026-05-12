def calculate_score(metrics: dict, config: dict) -> float:
    score = (100 - (metrics['cpu_percent'] * config['health']['weights']['cpu']) - 
             (metrics['ram_percent'] * config['health']['weights']['ram']) - 
             (metrics['disk_percent'] * config['health']['weights']['disk']))    
    return round(max(0.0, min(100.0, score)), 2)
