import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from VaccinationsDashboard import VaccinationsDashboard


class VaccinationsDashboardBuilder(DashboardBuilder):
    def __init__(self, datasets):
        self.dashboard = VaccinationsDashboard({key: value.set_index('date') for key, value in datasets.items()})
    
    def build(self):
        fig, axes = plt.subplots(3, 3, figsize=(30, 35))
        self.dashboard.showCumulativeVaccinationsPieChart(axes[0, 0])
        self.dashboard.showCumulativeVaccinationsByDoseBarChart(axes[0, 1])
        self.dashboard.showCumulativeVaccinationsByDoseTimeSeries(axes[0, 2])
        self.dashboard.showCumulativeVaccinationsTimeSeries(axes[1, 0])
        self.dashboard.showNewVaccinationsTimeSeries(axes[1, 1])
        self.dashboard.showNewFirstDoseVaccinationsTimeSeries(axes[1, 2])
        
        if 'by_manufacturer' in self.dashboard.datasets.keys():
            self.dashboard.showWeeklyVaccinationsByManufacturerTimeSeries(axes[2, 0])
            self.dashboard.showCumulativeVaccinationsByManufacturerBarChart(axes[2, 1])
        else:
            axes[2, 0].axis('off')
            axes[2, 1].axis('off')
        if 'by_age' in self.dashboard.datasets.keys():
            self.dashboard.showCumulativeVaccinationsByAgeBarChart(axes[2, 2])
        else:
            axes[2, 2].axis('off')
        plt.subplots_adjust(wspace=0.5, hspace=0.9)
        plt.show()