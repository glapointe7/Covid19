import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from SummaryDataset import SummaryDataset
from Dashboard import Dashboard


class TopCountriesDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)
        
    def showNewCases(self, ax):
        dataset = self.datasets.topCountriesOn(feature='new_cases', top_n=10)
        dataset.plot.bar(legend=False, ax=ax, rot=90)
        
        ax.set_xlabel('')
        ax.set_ylabel('New Cases', fontdict={'fontsize': 12})
        
        for bar in ax.patches:
            bar_height = int(bar.get_height())
            ax.text(x=bar.get_x(), y=1.01*bar_height, s=str(bar_height), fontdict={'fontsize': 11})
            
    def showNewDeaths(self, ax):
        dataset = self.datasets.topCountriesOn(feature='new_deaths', top_n=10)
        dataset.plot.bar(legend=False, ax=ax, rot=90)
        
        ax.set_xlabel('')
        ax.set_ylabel('New Deaths', fontdict={'fontsize': 12})
        
        for bar in ax.patches:
            bar_height = int(bar.get_height())
            ax.text(x=bar.get_x(), y=1.01*bar_height, s=str(bar_height), fontdict={'fontsize': 11})
            
    def showSecondDoseVaccination(self, ax):
        dataset = self.datasets.topCountriesOn(feature='people_2nd_dose_%', top_n=10)
        dataset.plot.bar(legend=False, ax=ax, rot=90)
        
        ax.set_xlabel('')
        ax.set_ylabel('People with 2nd Dose %', fontdict={'fontsize': 12})
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        
        for bar in ax.patches:
            bar_height = bar.get_height()
            ax.text(x=bar.get_x(), y=1.01*bar_height, s=str(bar_height), fontdict={'fontsize': 11})
            
    def showDeathsOverCases(self, ax):
        dataset = self.datasets.topCountriesOn(feature='deaths_over_cases_%', top_n=10)
        dataset.plot.bar(legend=False, ax=ax, rot=90)
        
        ax.set_xlabel('')
        ax.set_ylabel('Cases over Deaths %', fontdict={'fontsize': 12})
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        
        for bar in ax.patches:
            bar_height = bar.get_height()
            ax.text(x=bar.get_x(), y=1.01*bar_height, s=str(bar_height), fontdict={'fontsize': 11})