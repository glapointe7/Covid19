import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from WorldMapDashboard import WorldMapDashboard


class WorldMapDashboardBuilder(DashboardBuilder):
    def __init__(self, datasets):
        self.dashboard = WorldMapDashboard(datasets)
    
    def build(self):
        fig, axes = plt.subplots(2, 2, figsize=(30, 30))
        self.dashboard.showCumulativeCases(axes[0, 0])
        self.dashboard.showCumulativeCasesOverPopulation(axes[0, 1])
        self.dashboard.showSecondDoseVaccinations(axes[1, 0])
        self.dashboard.showDeathOverPopulation(axes[1, 1])
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.tight_layout()
        plt.show()