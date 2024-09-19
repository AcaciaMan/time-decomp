# add class DecompositionSingleton
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
from enum import Enum

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
            self.plot_params = {}
            plt.rcParams['figure.figsize'] = [19.20,10.80]
            self.colors = ['#636efa', '#EF553B', '#00cc96', '#ab63fa', '#FFA15A'] 
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

    def get_colors_array(self, n):
        # get n colors from a color map
        return plt.get_cmap('tab20', n).colors
    
    class ChartElement(Enum):
        OBSERVED = 'observed'
        SEASONAL = 'seasonal'
        TREND = 'trend'
        RESID = 'resid'

    def check_chart_elements(self, chart_elements):

        # check if chart elements are valid
        for ce in chart_elements:
            if ce not in [self.ChartElement.OBSERVED, self.ChartElement.SEASONAL, self.ChartElement.TREND, self.ChartElement.RESID]:
                raise ValueError(f"Invalid chart element: {ce}")
            
        if self.ChartElement.OBSERVED in chart_elements and self.ChartElement.TREND in chart_elements:
            raise ValueError("Cannot plot both observed and trend elements")
        if self.ChartElement.OBSERVED in chart_elements and self.ChartElement.RESID in chart_elements:
            raise ValueError("Cannot plot both observed and resid elements")
        if self.ChartElement.TREND in chart_elements and self.ChartElement.RESID in chart_elements:
            raise ValueError("Cannot plot both trend and resid elements")


    def plot_decomposition(self, feature,  range_column, range_data, data_column, title, xlabel = None, ylabel = None, chart_elements = [ChartElement.SEASONAL, ChartElement.TREND]):

        # check if chart elements are valid
        self.check_chart_elements(chart_elements)

        if xlabel is None:
            xlabel = data_column
        if ylabel is None:
            ylabel = feature

        # plot the decomposition of a feature for a data range of range column for a data column
        plt.figure()
        # get colors for the range data
        if len(self.colors) < len(range_data):
            self.colors = self.get_colors_array(len(range_data))

        # plot the first data of the range
        for i, n in enumerate(range_data):
            if self.ChartElement.OBSERVED in chart_elements:
                if self.ChartElement.SEASONAL in chart_elements:
                    if i == 0:
                        # get mean of the trend
                        n_trend = self.s[feature].observed[self.df[range_column] == n].mean()
                        plt.plot(self.df[self.df[range_column] == n][data_column], self.s[feature].seasonal[self.df[range_column] == n]+n_trend, color='red', linewidth=2, label='Seasonality')
                plt.plot(self.df[self.df[range_column] == n][data_column], self.s[feature].observed[self.df[range_column] == n], color=self.colors[i], label=str(n))


            elif self.ChartElement.TREND in chart_elements:
                if self.ChartElement.SEASONAL in chart_elements:
                    if i == 0:
                        # get mean of the trend
                        n_trend = self.s[feature].trend[self.df[range_column] == n].mean()
                        plt.plot(self.df[self.df[range_column] == n][data_column], self.s[feature].seasonal[self.df[range_column] == n]+n_trend, color='red', linewidth=2, label='Seasonality')
                plt.plot(self.df[self.df[range_column] == n][data_column], self.s[feature].trend[self.df[range_column] == n], color=self.colors[i], label=str(n))

            elif self.ChartElement.RESID in chart_elements:
                if self.ChartElement.SEASONAL in chart_elements:
                    if i == 0:
                        plt.plot(self.df[self.df[range_column] == n][data_column], self.s[feature].seasonal[self.df[range_column] == n], color='red', linewidth=2, label='Seasonality')
                plt.plot(self.df[self.df[range_column] == n][data_column], self.s[feature].resid[self.df[range_column] == n], color=self.colors[i], label=str(n))


            elif self.ChartElement.SEASONAL in chart_elements:
                if i == 0:
                    plt.plot(self.df[self.df[range_column] == n][data_column], self.s[feature].seasonal[self.df[range_column] == n], color='red', linewidth=2, label='Seasonality')
   

        font1 = {'family':'serif','color':'blue','size':32}
        font2 = {'family':'serif','color':'darkred','size':24}  
        
        plt.title(title, fontdict = font1, loc = 'left')
        plt.xlabel(xlabel, fontdict = font2)
        plt.ylabel(ylabel, fontdict = font2)  

        plt.legend(loc='best', ncol=3, fancybox=True, shadow=True, fontsize="24" )

        plt.xticks(fontsize = 20)
        plt.yticks(fontsize = 20)
