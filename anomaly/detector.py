from db.storage import get_baseline_avarage


def check_anomaly(metric_name : str, current_value : float, config : dict) -> bool:
    baseline_avarage = get_baseline_avarage(metric_name, 60) #window hardcoded to change later
    try:
        return current_value > (baseline_avarage * config['anomaly']['multiplier'])
    except Exception as e:
        print(f'An error occured {e}')
        return False