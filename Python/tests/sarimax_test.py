# We will test the Sarimax class in this file


from matplotlib import pyplot as plt
from time_decomp.decomposition import DecompositionSingleton
from time_decomp.sarimax import Sarimax
import unittest

import pandas as pd

class TestSarimax(unittest.TestCase):
    
    def setUp(self):
        self.decomp = Sarimax()
        # create dataframe with 10 periods and name column 'data'
        self.decomp.data = pd.DataFrame({'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

        # concatenate 10 periods to create 48 periods
        for i in range(4):
            self.decomp.data = pd.concat([self.decomp.data, self.decomp.data], ignore_index=True)

        # create series with 48 periods
        self.decomp.data = self.decomp.data.rename(columns={0: 'data'}).reset_index(drop=True)
        self.decomp.data.index = pd.date_range(start='1-1-2021', periods=160, freq='D')
        self.decomp.data = self.decomp.data['data']
        print(self.decomp.data.head(5), flush=True)
        self.decomp.sarimax_params = {'order': (1, 1, 1), 'seasonal_order': (1, 1, 1, 10)}

    def test_fit(self):
        self.decomp.fit()
        self.assertIsNotNone(self.decomp.fitted_model)

    def test_predict(self):
        self.decomp.fit()
        self.decomp.predict()
        self.assertIsNotNone(self.decomp.forecast)
        self.assertIsNotNone(self.decomp.forecast_index)
        self.assertIsNotNone(self.decomp.forecast_series)

    def test_plot(self):
        self.decomp.fit()
        self.decomp.predict()
        self.decomp.plot()
        self.assertIsNotNone(self.decomp.forecast)
        self.assertIsNotNone(self.decomp.forecast_index)
        self.assertIsNotNone(self.decomp.forecast_series)
        plt.show()

    def test_plot_keew(self):
        self.decomp = Sarimax()
        # create dataframe with 10 periods and name column 'data'
        self.decomp.data = pd.DataFrame({'data': [1, 2, 3, 4]})

        # concatenate 10 periods to create 48 periods
        for i in range(10):
            self.decomp.data = pd.concat([self.decomp.data, self.decomp.data], ignore_index=True)

        # create series with 48 periods
        self.decomp.data = self.decomp.data.rename(columns={0: 'data'}).reset_index(drop=True)
        self.decomp.data['Date'] = pd.date_range(start='1-1-2021', periods=4096, freq='D')
        self.decomp.data['Year'] = self.decomp.data['Date'].dt.year
        self.decomp.data['Month'] = self.decomp.data['Date'].dt.month

        self.decomp.data['KeewMonth'] = self.decomp.data['Date'].apply(DecompositionSingleton().get_month_keew)
        self.decomp.data['Keew']=(self.decomp.data['Month']-1)*4+self.decomp.data['KeewMonth']

        self.decomp.data = self.decomp.data.groupby(['Year', 'Keew']).last().reset_index()

        self.decomp.data['Date'] = pd.to_datetime('2020-01-01') + pd.to_timedelta(self.decomp.data.index, unit='D')
        self.decomp.data = self.decomp.data.set_index('Date').drop(columns=['Year', 'Keew'])
        self.decomp.data = self.decomp.data.asfreq('D')

        self.decomp.data = self.decomp.data['data']
        print(self.decomp.data.head(5), flush=True)
        self.decomp.sarimax_params = {'order': (1, 1, 1), 'seasonal_order': (1, 1, 1, 48)}



        self.decomp.fit()
        self.decomp.predict()
        self.decomp.plot()
        self.assertIsNotNone(self.decomp.forecast)
        self.assertIsNotNone(self.decomp.forecast_index)
        self.assertIsNotNone(self.decomp.forecast_series)
        print(self.decomp.fitted_model.summary(), flush=True)
        plt.show()