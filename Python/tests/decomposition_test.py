# create test
# test_decomposition.py
import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time_decomp.decomposition import DecompositionSingleton
from statsmodels.tsa.seasonal import DecomposeResult


# Configure logging
print("Configuring logging")

class TestDecompositionSingleton(unittest.TestCase):
    def setUp(self):
        self.decomp = DecompositionSingleton()

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

        
        self.decomp.features = ['A', 'B']
        self.decomp.decompose_params = {'model': 'additive', 'period':12, 'extrapolate_trend':'freq'}
        self.decomp.plot_params = {'title': 'Decomposition of feature', 'xlabel': 'Time', 'ylabel': 'Feature'}

    def test_m_decompose(self):
        self.decomp.m_decompose()
        self.assertTrue(all([isinstance(self.decomp.s[c], DecomposeResult) for c in self.decomp.features]))

    def test_get_colors_array(self):
        self.assertEqual(len(self.decomp.get_colors_array(5)), 5)
        self.assertEqual(len(self.decomp.get_colors_array(10)), 10)
        self.assertEqual(len(self.decomp.get_colors_array(20)), 20)

    def test_plot_decomposition(self):

        # output df info
        print("Starting test_plot_decomposition")
        print("DataFrame Info:")
        print(self.decomp.df.info())
        print("DataFrame Head:")
        print("\n%s", self.decomp.df.head())

    
        self.decomp.m_decompose()
        self.decomp.plot_decomposition('A', 'Year', range(2022,2024), 'Month', 'A')
        plt.show()



if __name__ == '__main__':
    unittest.main()        