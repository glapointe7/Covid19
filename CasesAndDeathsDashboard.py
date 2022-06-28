import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from Dashboard import Dashboard


class CasesAndDeathsDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)

    def showTimeSeries(self, feature, ax):
        self.datasets[feature].plot(label=feature, ax=ax, rot=90)
    
        ax.set_ylabel(feature, fontdict={'fontsize': 16})
        ax.set_xlabel('')
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))