import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from CasesAndDeathsDashboard import CasesAndDeathsDashboard


class CasesAndDeathsDashboardBuilder(DashboardBuilder):
    def __init__(self, datasets):
        self.dashboard = CasesAndDeathsDashboard(datasets.set_index('date'))
    
    def build(self):
        fig, axes = plt.subplots(3, 2, figsize=(25, 15))
        self.dashboard.showTimeSeries('cumulative_cases', axes[0, 0])
        self.dashboard.showTimeSeries('cumulative_deaths', axes[0, 1])
        self.dashboard.showTimeSeries('new_cases', axes[1, 0])
        self.dashboard.showTimeSeries('new_deaths', axes[1, 1])
        self.dashboard.showTimeSeries('deaths_over_cases_%', axes[2, 0])
        axes[2, 1].axis('off')
        plt.subplots_adjust(hspace=0.5)
        plt.show()
