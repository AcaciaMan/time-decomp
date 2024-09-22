# tests for environmentaltrends.py

import unittest
import pandas as pd
import numpy as np
from time_decomp.environmentaltrends import EnvironmentalTrends

# Set pandas option to display all columns
pd.set_option('display.max_columns', None)

class TestEnvironmentalTrends(unittest.TestCase):

    def setUp(self):
        self.decomp = EnvironmentalTrends()

        self.decomp.df = pd.DataFrame({'A': np.random.randint(0,100, size=(100,)), 'B': np.random.randint(0,100, size=(100,))})


        lsYears = [2019]*100
        lsMonths = [1]*50 + [2]*50

        iYear = 2021
        iMonth = 1
        for i in range(100):
            if iMonth > 12:
                iYear += 1
                iMonth = 1
            lsYears[i] = iYear
            lsMonths[i] = iMonth
            iMonth += 1

        self.decomp.df['Year'] = lsYears
        self.decomp.df['Month'] = lsMonths    

        
        self.decomp.features = ['A']
        self.decomp.trend_data_params = {'year_col':'Year', 'month_col':'Month' }
        self.decomp.trends_params = {'seasons_per_year': 12, 'trend_lengths': [1], 'end_years': [2025]}

    def test_m_trends(self):
        self.decomp.m_trends()
        # output df info
        print("Starting test_plot_decomposition")
        print("DataFrame Info:")
        print(self.decomp.t['A'].info())
        print("DataFrame Head:")
        print("\n%s", self.decomp.t['A'].head())
