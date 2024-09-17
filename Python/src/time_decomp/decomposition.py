# add class DecompositionSingleton
import pandas as pd
import statsmodels.api as sm

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
            self.initialized = True

    def m_decompose(self):
        # from dictionary self.decompose_params, get the parameters for seasonal decomposition
        # apply seasonal decomposition on each feature in self.features
        for c in self.features:
            self.s[c] = sm.tsa.seasonal_decompose(self.df.loc[:,c], **self.decompose_params)


