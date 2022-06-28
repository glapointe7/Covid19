import matplotlib.pyplot as plt
from DashboardBuilder import DashboardBuilder
from OutliersDashboard import OutliersDashboard


class OutliersDashboardBuilder(DashboardBuilder):
    def __init__(self, datasets):
        self.dashboard = OutliersDashboardB(datasets)
    
    def build(self):
