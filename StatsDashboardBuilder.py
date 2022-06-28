import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from StatsDashboard import StatsDashboard


class StatsDashboardBuilder(DashboardBuilder):
    def __init__(self, datasets):
        self.dashboard = StatsDashboard(datasets)
    
    def build(self):
        fig, axes = plt.subplots(2, 3, figsize=(25, 15))
        self.dashboard.showCountriesDeathsOverCasesBoxPlot(axes[0, 0])
        self.dashboard.showLogCasesAndDeathsRegression(axes[0, 1])
        self.dashboard.showCasesOverPopulationPercentByPoverty(axes[0, 2])
        self.dashboard.showDeathsOverPopulationPercentByPoverty(axes[1, 0])
        self.dashboard.showPeopleVaccinatedBasedOnCasesPercent(axes[1, 1])
        self.dashboard.showPeopleVaccinatedPercentByPoverty(axes[1, 2])
        plt.show()