# add class DecompositionSingleton
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

class DecompositionSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DecompositionSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.df = pd.DataFrame()
            self.features = []
            self.s = {}
            self.decompose_params = {}
            plt.rcParams['figure.figsize'] = [12, 9]
            self.initialized = True

    def m_decompose(self):
        # from dictionary self.decompose_params, get the parameters for seasonal decomposition
        # apply seasonal decomposition on each feature in self.features
        for c in self.features:
            self.s[c] = sm.tsa.seasonal_decompose(self.df.loc[:,c], **self.decompose_params)


    def get_month_keew(self, x):
        if x.day <= 7:
            return 1
        if x.day >= 8 and x.day <= 15:
            return 2
        if x.month == 2:
            if x.day >= 23:
                return 4
            else:
                return 3
        else:
            if x.day >= 24:
                return 4
            else:
                return 3        
