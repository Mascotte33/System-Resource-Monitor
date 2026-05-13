import time
from dotenv import load_dotenv
import os, yaml
from anomaly.detector import check_anomaly
from collector.metrics import collect_metrics
from db.storage import add_baseline, init_db
from health.score import calculate_score 

load_dotenv()

with open("config.yaml") as file:
    config = yaml.safe_load(file)

config["DISCORD_WEBHOOK_URL"] = os.environ.get("DISCORD_WEBHOOK_URL")

if __name__ == "__main__":
    init_db()
    while True:
        try:
            metrics = collect_metrics()
            print(metrics)
            print(f"Health Score: {calculate_score(metrics, config)}")     

            add_baseline('cpu_percent', metrics['cpu_percent'])
            add_baseline('ram_percent', metrics['ram_percent'])
            add_baseline('disk_percent', metrics['disk_percent'])

            if check_anomaly('cpu_percent', metrics['cpu_percent'], config):
                print ('Anomaly! cpu_percent spike detected!')
            if check_anomaly('ram_percent', metrics['ram_percent'], config):
                print ('Anomaly! ram_percent spike detected!')
            if check_anomaly('disk_percent', metrics['disk_percent'], config):
                print ('Anomaly! disk_percent spike detected!')
                
            time.sleep(config["collection"]["interval_seconds"])
            
        except KeyboardInterrupt:
            print("Stopped")
            break

        except Exception as e:
            print(f"Cycle Failed... \n {e}")
            
