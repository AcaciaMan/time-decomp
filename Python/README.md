# time-decomp
Time series decomposition plot trend and seasonality

Plot trend and seasonality together in one chart as described at [Business Days Time Series Weekly Trend and Seasonality](https://www.mdpi.com/2673-4591/5/1/26).

Example usage from ./Python/tests/keew_decomp_test.py

```
# create test
# test_decomposition.py
import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time_decomp.decomposition import DecompositionSingleton

class TestKeewDecomposition(unittest.TestCase):
    def setUp(self):
        self.decomp = DecompositionSingleton()

        n = 2000

        df = pd.DataFrame({'A': np.random.randint(0,100, size=(n,)), 'B': np.random.randint(0,100, size=(n,))})

        lsDays = [pd.Timestamp(2021, 1, 1)]*n
        for i in range(n):
            # construct time, where iYear-iMonth-i
            lsDays[i] = pd.Timestamp( np.random.randint(2021,2025), np.random.randint(1,13) , (i+1) % 28 + 1)    

        df['Day'] = lsDays

        df['Year'] = df['Day'].dt.year
        df['Month'] = df['Day'].dt.month
        df['KeewMonth'] = df['Day'].apply(self.decomp.get_month_keew)
        df['Keew']=(df['Month']-1)*4+df['KeewMonth']

        self.decomp.df = df.groupby(['Year', 'Keew']).last().reset_index()
        
        self.decomp.features = ['A', 'B']
        self.decomp.decompose_params = {'model': 'additive', 'period':48, 'extrapolate_trend':'freq'}        

    def test_plot_decomposition(self):

        # output df info
        print("Starting test_plot_decomposition")
        print("DataFrame Info:")
        print(self.decomp.df.info())
        print("DataFrame Head:")
        print("\n%s", self.decomp.df.head())

    
        self.decomp.m_decompose()
        self.decomp.plot_decomposition('A', 'Year', range(2021,2025), 'Keew', 'A keew', chart_elements=[self.decomp.ChartElement.TREND, self.decomp.ChartElement.SEASONAL])
        plt.show()

```

## Added PLOTLY to run from IPython Notebook

```
from plotly.offline import iplot

decomp.m_decompose()
fig = decomp.plot_decomposition_plotly('A', 'Year', range(2021,2025), 'Keew', 'A keew', chart_elements=[ decomp.ChartElement.OBSERVED, decomp.ChartElement.SEASONAL])
iplot(fig)
```
