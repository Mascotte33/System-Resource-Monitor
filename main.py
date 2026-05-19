import time
from dotenv import load_dotenv
import os, yaml
from config.logger_config import logger 
from alerts.discord import send_discord_alert
from anomaly.detector import check_anomaly
from collector.metrics import collect_metrics
from db.storage import add_anomalies, add_baseline, init_db
from exporter import increment_anomaly_counter, start_exporter, update_metrics
from health.score import calculate_score 


load_dotenv()

with open("config/config.yaml") as file:
    config = yaml.safe_load(file)

if config == None:
    logger.critical('config.yml file is missing, exiting')
    quit()

config["alerts"]['discord']['webhook_url'] = os.environ.get("DISCORD_WEBHOOK_URL")


if __name__ == "__main__":
    init_db()    
    start_exporter(config['exporter']['port'])
    while True:
        try:
            metrics = collect_metrics()
            offender_process = metrics['top_ten_processes'][0]['name']
            health_score = calculate_score(metrics, config)
            logger.info(f'Health Score: {health_score}')            

            add_baseline('cpu_percent', metrics['cpu_percent'])
            add_baseline('ram_percent', metrics['ram_percent'])
            add_baseline('disk_percent', metrics['disk_percent'])

            if check_anomaly('cpu_percent', metrics['cpu_percent'], config):
                message = {"content": f"🚨 CPU spike detected: {metrics['cpu_percent']}%"}
                send_discord_alert(message, config)
                increment_anomaly_counter('cpu_percent')   
                add_anomalies('cpu_percent', metrics['cpu_percent'], offender_process, config) 
            
            if check_anomaly('ram_percent', metrics['ram_percent'], config):
                message = {"content": f"🚨 RAM spike detected: {metrics['ram_percent']}%"}
                send_discord_alert(message, config)
                increment_anomaly_counter('ram_percent')     
                add_anomalies('ram_percent', metrics['ram_percent'],offender_process , config) 
          

            if check_anomaly('disk_percent', metrics['disk_percent'], config):
                message = {"content": f"🚨 Disk spike detected: {metrics['disk_percent']}%"}
                send_discord_alert(message, config)
                increment_anomaly_counter('disk_percent')   
                add_anomalies('disk_percent', metrics['disk_percent'],offender_process , config)          
            
            update_metrics(metrics, health_score)

            time.sleep(config["collection"]["interval_seconds"])

        except KeyboardInterrupt:
            logger.info('System Resource Monitor shutting down gracefully.')
            break

        except Exception as e:
            logger.error(f'Cycle failed... \n {e}')
            
