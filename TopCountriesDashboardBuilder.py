import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from TopCountriesDashboard import TopCountriesDashboard


class TopCountriesDashboardBuilder(DashboardBuilder):
    def __init__(self, dataset):
        self.dashboard = TopCountriesDashboard(dataset)
    
    def build(self):
        fig, axes = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle('Top Countries', fontsize=20)
        self.dashboard.showNewCases(ax=axes[0, 0])
        self.dashboard.showNewDeaths(ax=axes[0, 1])
        self.dashboard.showSecondDoseVaccination(ax=axes[1, 0])
        self.dashboard.showDeathsOverCases(ax=axes[1, 1])
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)
        plt.show()
