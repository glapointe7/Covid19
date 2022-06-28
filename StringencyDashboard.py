import matplotlib.pyplot as plt
from Dashboard import Dashboard


class StringencyDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)

    def showIndexes(self, ax):
        self.datasets['stringency_index'].plot(label='Stringency Index', ax=ax, rot=90, legend=True)
        self.datasets['government_response_index'].plot(label='Government Response Index', ax=ax, rot=90, legend=True)
    
        ax.set_ylabel('Index', fontdict={'fontsize': 16})
        ax.set_xlabel('')