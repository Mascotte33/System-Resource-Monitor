import time
import requests
from config.logger_config import logger


def send_discord_alert(message : dict, config : dict) -> bool:  
    try:
        if config['alerts']['discord']['enabled']:
                for i in range(3):
                    response = requests.post(config['alerts']['discord']['webhook_url'], json=message, timeout=5)
                    if response.status_code == 200 or response.status_code == 204:
                        return True
                    else:
                        time.sleep(5)
                else:
                    logger.error('Failed to send discord warning!')
                    return False
        else:
            logger.warning('Discord messaging is turned off')
            return False
    except Exception as e:
        logger.exception(f'Error occured: \n {e}')
        return False