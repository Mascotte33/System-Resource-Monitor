import time
from dotenv import load_dotenv
import os, yaml
from alerts.discord import send_discord_alert
from anomaly.detector import check_anomaly
from collector.metrics import collect_metrics
from db.storage import add_baseline, init_db
from exporter import increment_anomaly_counter, start_exporter, update_metrics
from health.score import calculate_score 

load_dotenv()

with open("config.yaml") as file:
    config = yaml.safe_load(file)

if config == None:
    print('config.yml file is missing. ')
    quit()

config["alerts"]['discord']['webhook_url'] = os.environ.get("DISCORD_WEBHOOK_URL")


if __name__ == "__main__":
    init_db()    
    start_exporter(config['prometheus']['port'])
    while True:
        try:
            metrics = collect_metrics()
            health_score = calculate_score(metrics, config)
            print(health_score)     

            add_baseline('cpu_percent', metrics['cpu_percent'])
            add_baseline('ram_percent', metrics['ram_percent'])
            add_baseline('disk_percent', metrics['disk_percent'])

            if check_anomaly('cpu_percent', metrics['cpu_percent'], config):
                message = {"content": f"🚨 CPU spike detected: {metrics['cpu_percent']}%"}
                send_discord_alert(message, config)
                increment_anomaly_counter('cpu_percent')               
            if check_anomaly('ram_percent', metrics['ram_percent'], config):
                message = {"content": f"🚨 RAM spike detected: {metrics['ram_percent']}%"}
                send_discord_alert(message, config)
                increment_anomaly_counter('ram_percent')               
            if check_anomaly('disk_percent', metrics['disk_percent'], config):
                message = {"content": f"🚨 Disk spike detected: {metrics['disk_percent']}%"}
                send_discord_alert(message, config)
                increment_anomaly_counter('disk_percent')             
            
            update_metrics(metrics, health_score)

            time.sleep(config["collection"]["interval_seconds"])

        except KeyboardInterrupt:
            print("Stopped")
            break

        except Exception as e:
            print(f"Cycle Failed... \n {e}")
            
