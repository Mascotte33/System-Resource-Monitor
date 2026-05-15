import unittest
from unittest.mock import patch

from anomaly.detector import check_anomaly
from health.score import calculate_score

class TestHealthScore(unittest.TestCase):
    def test_calculate_score_uses_weighted_penalties(self):
        metrics = { 
            'cpu_percent' : 10,
            'ram_percent' : 20,
            'disk_percent' : 30,
        }

        config = {
            'health' : {
                'weights' : {
                    'cpu' : 0.40,
                    'ram' : 0.30,
                    'disk' : 0.20
                } 
            }         
        }
        self.assertEqual(calculate_score(metrics, config),84.0)
    
    def test_calculate_score_clamps_to_zero(self):
        metrics = { 
            'cpu_percent' : 100,
            'ram_percent' : 20,
            'disk_percent' : 30,
        }

        config = {
            'health' : {
                'weights' : {
                    'cpu' : 1,
                    'ram' : 0.30,
                    'disk' : 0.20
                } 
            }         
        }
        self.assertEqual(calculate_score(metrics,config),0.0)


class TestAnomalyDetection(unittest.TestCase):
    def test_check_anomaly_returns_true_above_treshhold(self):
        config = {
            'collection' : {
                'baseline_window' : 60                
            },
            'anomaly' : {
                'multiplier' : 3
            }
        }
        with patch('anomaly.detector.get_baseline_avarage', return_value=20.0):
            self.assertFalse(check_anomaly('cpu_percent', 59.0, config))




    def test_check_anomaly_returns_false_below_treshhold(self):
        config = {
            'collection' : {
                'baseline_window' : 60                
            },
            'anomaly' : {
                'multiplier' : 3
            }
        }
        with patch('anomaly.detector.get_baseline_avarage', return_value=20.0):
            self.assertTrue(check_anomaly('cpu_percent', 61.0, config))

