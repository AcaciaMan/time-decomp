# class for environmental trends library implementation, extends DecompositionSingltone

import environmentaltrends as et
from time_decomp.decomposition import DecompositionSingleton

class EnvironmentalTrends(DecompositionSingleton):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EnvironmentalTrends, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.trend_data_params = {}
            self.trends_params = {}
            self.t = {}

            self.initialized = True


    def m_trends(self):

        self.trend_data_params['data'] = self.df

        for feature in self.features:
            self.trend_data_params['value_col'] = feature
            trend_data = et.TrendData(**self.trend_data_params)
            self.t[feature] = trend_data.trends(**self.trends_params)

