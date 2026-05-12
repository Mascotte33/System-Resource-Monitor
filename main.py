import time

from dotenv import load_dotenv
import os, yaml
from collector.metrics import collect_metrics
from health.score import calculate_score 

load_dotenv()

with open("config.yaml") as file:
    config = yaml.safe_load(file)

config["DISCORD_WEBHOOK_URL"] = os.environ.get("DISCORD_WEBHOOK_URL")

if __name__ == "__main__":

    while True:
        try:
            metrics = collect_metrics()
            print(metrics)
            print(f"Health Score: {calculate_score(metrics, config)}")
            time.sleep(config["collection"]["interval_seconds"])
            
        except KeyboardInterrupt:
            print("Stopped")
            break

        except Exception as e:
            print(f"Cycle Failed... \n {e}")
            
