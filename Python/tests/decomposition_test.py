# create test
# test_decomposition.py
import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.time_decomp.decomposition import DecompositionSingleton
from statsmodels.tsa.seasonal import DecomposeResult
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class TestDecompositionSingleton(unittest.TestCase):
    def setUp(self):
        self.decomp = DecompositionSingleton()
        self.decomp.df = pd.DataFrame({'A': np.random.randn(100), 'B': np.random.randn(100)})
        self.decomp.features = ['A', 'B']
        self.decomp.decompose_params = {'model': 'additive', 'period':12, 'extrapolate_trend':'freq'}
        self.decomp.plot_params = {'title': 'Decomposition of feature', 'xlabel': 'Time', 'ylabel': 'Feature'}

    def test_m_decompose(self):
        self.decomp.m_decompose()
        self.assertTrue(all([isinstance(self.decomp.s[c], DecomposeResult) for c in self.decomp.features]))

    def test_get_month_keew(self):
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-01-01')), 1)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-01-08')), 2)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-01-16')), 3)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-01-24')), 4)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-01-31')), 4)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-02-01')), 1)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-02-08')), 2)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-02-16')), 3)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-02-24')), 4)
        self.assertEqual(self.decomp.get_month_keew(pd.Timestamp('2020-02-29')), 4)

    def test_get_colors_array(self):
        self.assertEqual(len(self.decomp.get_colors_array(5)), 5)
        self.assertEqual(len(self.decomp.get_colors_array(10)), 10)
        self.assertEqual(len(self.decomp.get_colors_array(20)), 20)

    def test_plot_decomposition(self):
        # output df info
        logging.debug("DataFrame Info:")
        #logging.debug(self.decomp.df.info())
        logging.debug("DataFrame Head:")
        #logging.debug("\n%s", self.decomp.df.head())

        
        self.decomp.m_decompose()
        self.decomp.plot_decomposition('A', 'A', range(10), 'A', 'A')
        self.decomp.plot_decomposition('B', 'B', 'B', 'B', 'B')
        plt.show()