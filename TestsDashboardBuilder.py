import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from TestsDashboard import TestsDashboard


class TestsDashboardBuilder(DashboardBuilder):
    def __init__(self, dataset):
        self.dashboard = TestsDashboard(dataset.set_index('date'))
    
    def build(self):
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        self.dashboard.showCumulativeTestsTimeSeries(axes[0])
        self.dashboard.showNewTestsTimeSeries(axes[1])
        plt.subplots_adjust(wspace=0.5)
        plt.show()
