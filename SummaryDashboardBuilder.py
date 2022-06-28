from DashboardBuilder import DashboardBuilder
from SummaryDashboard import SummaryDashboard

import Utils
Utils.installPackageIfNotInstalled("plotly")
import plotly.graph_objects as go


class SummaryDashboardBuilder(DashboardBuilder):
    def __init__(self, dataset):
        self.dashboard = SummaryDashboard(dataset)
    
    def build(self):
        fig = go.Figure()
        self.dashboard.showLatestCases(fig)
        self.dashboard.showLatestDeaths(fig)
        self.dashboard.showCasesOverPopulation(fig)
        self.dashboard.showPeopleWithAtLeast2ndDose(fig)
        fig.update_layout(grid = {'rows': 2, 'columns': 2, 'pattern': "independent"})
        fig.show()
