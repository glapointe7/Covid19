import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from Dashboard import Dashboard
import Utils


class TestsDashboard(Dashboard):
    def __init__(self, datasets):
        super().__init__(datasets)
        
    def showCumulativeTestsTimeSeries(self, ax):
        self.datasets['cumulative_total'].plot(label="Total Tests", ax=ax, rot=90)
        
        ax.set_xlabel('Date', fontdict={'fontsize': 14})
        ax.set_ylabel('Number of tests', fontdict={'fontsize': 14})
        ax.set_title("Time series of the cumulative number of tests", fontdict={'fontsize': 16})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        
    def showNewTestsTimeSeries(self, ax):
        self.datasets['new_tests'].plot(label="New Tests", ax=ax, rot=90)
        
        ax.set_xlabel('Date', fontdict={'fontsize': 14})
        ax.set_ylabel('Number of new tests', fontdict={'fontsize': 14})
        ax.set_title("Time series of the number of new tests", fontdict={'fontsize': 16})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))