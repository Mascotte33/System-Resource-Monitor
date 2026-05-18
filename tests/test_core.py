import datetime
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from anomaly.detector import check_anomaly
from db.storage import add_anomalies, add_baseline, get_baseline_avarage, init_db
from health.score import calculate_score

class TestHealthScore(unittest.TestCase):
    def test_calculate_score_uses_weighted_penalties(self):
        metrics = { 
            'cpu_percent' : 10.0,
            'ram_percent' : 20.0,
            'disk_percent' : 30.0,
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
            'cpu_percent' : 100.0,
            'ram_percent' : 20.0,
            'disk_percent' : 30.0,
        }

        config = {
            'health' : {
                'weights' : {
                    'cpu' : 1.0,
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
            self.assertTrue(check_anomaly('cpu_percent', 61.0, config))




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
            self.assertFalse(check_anomaly('cpu_percent', 59.0, config))

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.previous_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        init_db()

    def tearDown(self):
        os.chdir(self.previous_cwd)
        self.temp_dir.cleanup()

    def test_add_baseline(self):
        add_baseline('cpu_percent', 13.0)
        connection = sqlite3.connect("monitor.db")
        cursor = connection.cursor()
        metric = cursor.execute('SELECT metric_name, value FROM baselines').fetchall()
        connection.close()

        self.assertEqual(metric, [('cpu_percent',13.0)])

    def tets_not_get_baseline_avarage(self):
        self.assertEqual(get_baseline_avarage('ram_percent', 60), 0.0)

    def test_get_baseline_avarage(self):
        add_baseline('cpu_percent', 10.0)
        add_baseline('cpu_percent', 20.0)
        add_baseline('cpu_percent', 30.0)
        avarage = get_baseline_avarage('cpu_percent', 60)
        self.assertEqual(avarage, 20.0)        

    def test_add_anomalies(self):
        add_baseline('cpu_percent', 10.0)
        add_baseline('cpu_percent', 20.0)
        config = {'collection' : {'baseline_window': 60}}
        add_anomalies('cpu_percent', 99.0, 'stress', config)

        connection = sqlite3.connect("monitor.db")
        cursor = connection.cursor()
        anomaly = cursor.execute('SELECT metric_name, value, avarage_value, offender_process from anomalies').fetchall()
        connection.close()

        self.assertEqual(len(anomaly), 1)
        self.assertEqual(anomaly[0][0], "cpu_percent")
        self.assertEqual(anomaly[0][1], 99.0)
        self.assertEqual(anomaly[0][2], 15.0)
        self.assertEqual(anomaly[0][3], 'stress')

if __name__ == "__main__":
    unittest.main()