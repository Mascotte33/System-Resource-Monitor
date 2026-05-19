import requests
from config.logger_config import logger

def send_discord_alert(message : dict, config : dict) -> bool:
    try:
        if config['alerts']['discord']['enabled']:
            response = requests.post(config['alerts']['discord']['webhook_url'], json=message, timeout=5)
            if response.status_code == 200 or response.status_code == 204:
                return True
            else:
                return False

        else:
            logger.info('Discord messagin is turned off')
            return False
    except Exception as e:
        logger.exception(f'Error occured: \n {e}')
        return False