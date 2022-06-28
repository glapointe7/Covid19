import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from HospitalizationsDashboard import HospitalizationsDashboard


class HospitalizationsDashboardBuilder(DashboardBuilder):
    def __init__(self, dataset):
        self.dashboard = HospitalizationsDashboard(dataset.groupby(['date', 'indicator'])['number_of_people'].first().unstack())
    
    def filterColumnsEndingWithMillion(self):
        columns = self.dashboard.datasets.columns.to_list()
        
        return list(filter(lambda column: column.endswith('million'), columns))

    
    def build(self):
        fig, axes = plt.subplots(1, 2, figsize=(20, 7))
        self.dashboard.showNewHospitalizationsTimeSeries(axes[0])
    
        columns = self.filterColumnsEndingWithMillion()
        if len(columns) > 0:
            self.dashboard.showHospitalizationsPerMillionBarChart(columns, axes[1])
        else:
            axes[1].axis('off')
        plt.subplots_adjust(wspace=0.6)
        plt.show()
