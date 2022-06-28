import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from StringencyDashboard import StringencyDashboard


class StringencyDashboardBuilder(DashboardBuilder):
    def __init__(self, datasets):
        self.dashboard = StringencyDashboard(datasets.set_index('date'))
    
    def build(self):
        fig, axes = plt.subplots(1, figsize=(15, 15))
        self.dashboard.showIndexes(axes)
        plt.show()