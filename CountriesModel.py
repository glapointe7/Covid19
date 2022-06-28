import pandas as pd


class CountriesModel:
    def __init__(self):
        self.countries = []
        
    def downloadCountriesDataset(url):
        self.countries = pd.read_csv(url, 
                                     index_col=False, 
                                     header=0, 
                                     usecols=['name', "alpha-3", "region"])
        self.countries = self.countries.rename({'name': 'entity', 'alpha-3': 'iso_code', 'region': 'continent'}, axis='columns') \
                                       .sort_values(by=['entity'], ascending=True)

    def addPopulationFeature(url):
        population = pd.read_csv(url, usecols=['entity', 'iso_code', 'population'])
        population = population.replace(regex=r'^OWID_', value='')
        self.countries = pd.merge(left=population, 
                                  right=self.countries, 
                                  on=['iso_code'], 
                                  how='inner')
                                  
    def addPovertyFeature(filename):
        poverty = pd.read_csv(filename, 
                              index_col=False, 
                              header=0, 
                              usecols=["SpatialDimValueCode", "IsLatestYear", "Value"])
        poverty = poverty.loc[poverty["IsLatestYear"] == True]
        poverty = poverty.drop(['IsLatestYear'], axis='columns')
        poverty = poverty.rename({'SpatialDimValueCode': 'iso_code', 'Value': 'poverty_%'}, axis='columns')
        
        self.countries = pd.merge(left=poverty, 
                                  right=self.countries, 
                                  how="right", 
                                  on=['iso_code'])
                                  
    def addDensityFeature(url, year):
        densities = pd.read_csv(url)
        densities = densities.rename({'Entity': 'entity', 'population_density': 'density'}, axis='columns')
        
        self.countries = pd.merge(left=densities.loc[densities['Year'] == year, ['entity', 'density']], 
                                  right=self.countries, 
                                  how="right", 
                                  on=['entity'])
