import Utils
Utils.installPackageIfNotInstalled("geoplot")
Utils.installPackageIfNotInstalled("geopandas")
import geoplot
import geopandas as gpd
import pandas as pd
from IPython.display import display
from  matplotlib.colors import LinearSegmentedColormap
from Dashboard import Dashboard


class WorldMapDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)

    def showCumulativeCases(self, ax):
        world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        self.datasets = self.datasets.rename(columns={'iso_code': 'iso_a3'})
        world_map = pd.merge(left=world_map,
                             right=self.datasets[['iso_a3', 'cumulative_cases']],
                             on=['iso_a3'],
                             how='left')
                             
        cmap = LinearSegmentedColormap.from_list('',["green", "yellow", "red"])
        world_map.plot(column='cumulative_cases', 
                       cmap=cmap,
                       legend=True,
                       legend_kwds={'shrink': 0.2},
                       ax=ax)
        ax.set_title('Cumulative Cases')
        ax.set_axis_off()
        
    def showCumulativeCasesOverPopulation(self, ax):
        world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        self.datasets = self.datasets.rename(columns={'iso_code': 'iso_a3'})
        world_map = pd.merge(left=world_map,
                             right=self.datasets[['iso_a3', 'cases_over_pop_%']],
                             on=['iso_a3'],
                             how='left')
                             
        cmap = LinearSegmentedColormap.from_list('',["green", "yellow", "red"])
        world_map.plot(column='cases_over_pop_%', 
                       cmap=cmap,
                       legend=True,
                       legend_kwds={'shrink': 0.2},
                       ax=ax)
        ax.set_title('Cumulative Cases Over Population Percentage')
        ax.set_axis_off()
        
    def showSecondDoseVaccinations(self, ax):
        world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        self.datasets = self.datasets.rename(columns={'iso_code': 'iso_a3'})
        world_map = pd.merge(left=world_map,
                             right=self.datasets[['iso_a3', 'people_2nd_dose_%']],
                             on=['iso_a3'],
                             how='left')
                             
        cmap = LinearSegmentedColormap.from_list('',["red", "yellow", "green"])
        world_map.plot(column='people_2nd_dose_%', 
                       cmap=cmap,
                       legend=True,
                       legend_kwds={'shrink': 0.2},
                       ax=ax)
        ax.set_title('Second Dose Vaccination Percentage')
        ax.set_axis_off()
        
    def showDeathOverPopulation(self, ax):
        world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        self.datasets = self.datasets.rename(columns={'iso_code': 'iso_a3'})
        world_map = pd.merge(left=world_map,
                             right=self.datasets[['iso_a3', 'deaths_over_pop_%']],
                             on=['iso_a3'],
                             how='left')
                             
        cmap = LinearSegmentedColormap.from_list('',["green", "yellow", "red"])
        world_map.plot(column='deaths_over_pop_%', 
                       cmap=cmap,
                       legend=True,
                       legend_kwds={'shrink': 0.2},
                       ax=ax)
        ax.set_title('Death Over Population Percentage')
        ax.set_axis_off()