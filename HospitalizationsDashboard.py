import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from Dashboard import Dashboard


class HospitalizationsDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)
    
    def showNewHospitalizationsTimeSeries(self, ax):
        columns = self.datasets.columns.to_list()
        columns = filter(lambda column: not column.endswith('million'), columns)
        for column in columns:
            self.datasets[column].plot(legend=True, ax=ax, rot=90)
    
        ax.set_xlabel('Date', fontdict={'fontsize': 16})
        ax.set_ylabel('Hospitalizations', fontdict={'fontsize': 16})
        ax.set_title("Time series of the number of new hospitalizations", fontdict={'fontsize': 20})
    
    def showHospitalizationsPerMillionBarChart(self, columns, ax):
        self.datasets[columns].iloc[-1].plot.barh()
        ax.set_xlabel('Hospitalizations per million', fontdict={'fontsize': 16})
        ax.set_title("Number of hospitalizations per million by type of hospitalization", fontdict={'fontsize': 20})
        
        for i, value in enumerate(self.datasets[columns].iloc[-1]):
            ax.text(x=value / 3, 
                    y=i, 
                    s=str(value), 
                    color='black', 
                    fontsize=14)
