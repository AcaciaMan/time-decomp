from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
import pandas as pd

class Sarimax:
    def __init__(self):
        self.data = None
        self.fitted_model = None
        self.model = None
        self.sarimax_params = {}
        self.forecast = None
        self.forecast_index = None
        self.forecast_series = None

    def fit(self):
        self.model = SARIMAX(self.data, **self.sarimax_params)
        self.fitted_model = self.model.fit()
        return self.fitted_model

    def predict(self):
        # Forecast the next 48 periods
        self.forecast = self.fitted_model.get_forecast(steps=48)
        self.forecast_index = pd.date_range(start=self.data.index[-1], periods=48)
        self.forecast_series = pd.Series(self.forecast.predicted_mean, index=self.forecast_index)

    def plot(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data, label='Observed')
        plt.plot(self.forecast_series, label='Forecast', color='red')
        plt.fill_between(self.forecast_series.index, self.forecast.conf_int().iloc[:, 0], self.forecast.conf_int().iloc[:, 1], color='pink')
        plt.legend()