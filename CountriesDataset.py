import pandas as pd
import numpy as np
from Dataset import Dataset


class CountriesDataset(Dataset):
    def unifyEntityNames(self, countries):
        countries_unified = {
            'Bolivia (Plurinational State of)': 'Bolivia',
            'Brunei Darussalam': 'Brunei',
            "Côte d'Ivoire": "Cote d'Ivoire",
            'Congo, Democratic Republic of the': 'Democratic Republic of Congo',
            'Iran (Islamic Republic of)': 'Iran',
            "Lao People's Democratic Republic": 'Laos',
            'Micronesia (Federated States of)': 'Micronesia',
            'Moldova, Republic of': 'Maldova',
            'Palestine, State of': 'Palestine',
            'Russian Federation': 'Russia',
            "Korea (Democratic People's Republic of)": 'North Korea',
            "Korea, Republic of": 'South Korea',
            'Syrian Arab Republic': 'Syria',
            'Taiwan, Province of China': 'Taiwan',
            'Tanzania, United Republic of': 'Tanzania',
            'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
            'United States of America': 'United States',
            'Venezuela (Bolivarian Republic of)': 'Venezuela',
            'Viet Nam': 'Vietnam'
        }
        
        countries['name'] = countries['name'].replace(countries_unified)
    
    '''
    SELECT name AS entity, alpha-3 AS iso_code, region AS continent
    FROM countries
    '''
    def queryCountriesDataset(self):
        url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
        countries = pd.read_csv(url, 
                                index_col=False, 
                                header=0, 
                                usecols=['name', "alpha-3", "region", "intermediate-region"])
        self.unifyEntityNames(countries)
        countries.loc[countries['intermediate-region'] == "South America", 'region'] = "South America"
        countries.loc[(countries['region'] == 'Americas') & (countries['intermediate-region'] != "South America"), 'region'] = "North America" 
        
        return countries.rename({'name': 'entity', 'alpha-3': 'iso_code', 'region': 'continent'}, axis='columns') \
                        .drop('intermediate-region', axis='columns')
    
    '''
    SELECT REGEXP_REPLACE(iso_code, 'OWID_', '') AS iso_code, population
    FROM population_latest
    '''
    def queryPopulationDataset(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/scripts/input/un/population_latest.csv"
        population = pd.read_csv(url, usecols=['iso_code', 'population'])
        
        # OWID iso codes to rename  
        iso_codes_owid = {
            'OWID_AFR': 'AF',
            'OWID_ASI': 'AS',
            'OWID_CIS': 'CIS',
            'OWID_EUR': 'EU',
            'OWID_EUN': 'EUUN',
            'OWID_HIC': 'HIIN',
            'OWID_KOS': 'KOS',
            'OWID_LIC': 'LOIN',
            'OWID_LMC': 'LOMI',
            'OWID_NAM': 'NA',
            'OWID_OCE': 'OC',
            'OWID_SAM': 'SA',
            'OWID_UMC': 'UPMI',
            'OWID_WRL': 'WR',
            'OWID_WEC': 'WREC'
        }
        population['iso_code'] = population['iso_code'].replace(iso_codes_owid)

        return population
        
    '''
    SELECT SpatialDimValueCode AS iso_code, Value AS poverty_percent
    FROM WorldPovertyIndex
    WHERE IsLatestYear = TRUE
    '''
    def queryPovertyDataset(self):
        filename = "WorldPovertyIndex.csv"
        poverty = pd.read_csv(filename, 
                              index_col=False, 
                              header=0, 
                              usecols=["SpatialDimValueCode", "IsLatestYear", "Value"])
                              
        return poverty.loc[poverty["IsLatestYear"] == True] \
                      .drop(['IsLatestYear'], axis='columns') \
                      .rename({'SpatialDimValueCode': 'iso_code', 'Value': 'poverty_%'}, axis='columns')

    '''
    SELECT Entity AS entity, population_density AS density
    FROM PopulationDensity
    WHERE Year = 2020
    '''
    def queryDensityDataset(self, year):
        url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Population%20density%20(World%20Bank%2C%20Gapminder%2C%20HYDE%20%26%20UN)/Population%20density%20(World%20Bank%2C%20Gapminder%2C%20HYDE%20%26%20UN).csv"
        densities = pd.read_csv(url)
        return densities.rename({'Entity': 'entity', 'population_density': 'density'}, axis='columns') \
                        .loc[densities['Year'] == year, ['entity', 'density']]
               
    '''
    SELECT C.entity, C.iso_code, C.continent, Pl.population, Wpi.poverty_percent, Pd.density
    FROM Countries AS C
        RIGHT JOIN population_latest AS Pl ON (C.iso_code = Pl.iso_code)
        LEFT JOIN WorldPovertyIndex AS Wpi ON (C.iso_code = Wpi.iso_code)
        LEFT JOIN PopulationDensity AS Pd ON (C.entity = Pd.entity)
    ORDER BY entity ASC
    '''         
    def prepare(self):
        self.dataset = self.queryCountriesDataset()
        population = self.queryPopulationDataset()
        self.dataset = pd.merge(left=self.dataset, 
                                right=population, 
                                on=['iso_code'], 
                                how='right')
        poverty = self.queryPovertyDataset()
        self.dataset = pd.merge(left=self.dataset, 
                                right=poverty, 
                                how='left', 
                                on=['iso_code'])
        density = self.queryDensityDataset(year=2020)
        self.dataset = pd.merge(left=self.dataset, 
                                right=density, 
                                how='left', 
                                on=['entity'])
        
        self.dataset.loc[self.dataset['iso_code'] == 'AF', 'continent'] = 'Africa'
        self.dataset.loc[self.dataset['iso_code'] == 'AS', 'continent'] = 'Asia'
        self.dataset.loc[self.dataset['iso_code'] == 'EU', 'continent'] = 'Europe'
        self.dataset.loc[self.dataset['iso_code'] == 'NA', 'continent'] = 'North America'
        self.dataset.loc[self.dataset['iso_code'] == 'SA', 'continent'] = 'South America'
        self.dataset.loc[self.dataset['iso_code'] == 'OC', 'continent'] = 'Oceania'
        self.dataset.loc[self.dataset['iso_code'] == 'WR', 'continent'] = 'World'
        
        self.dataset = self.dataset.sort_values(by=['entity'], ascending=True)
        
        
    def getEntityList(self):
        return list(zip(self.dataset['entity'].dropna(), self.dataset['iso_code'].dropna()))
        
    def getEntityNameFromISOCode(self, iso_code):
        return self.dataset.loc[self.dataset['iso_code'] == iso_code, 'entity'].iloc[0]
        
    def getContinentNameFromISOCode(self, iso_code):
        return self.dataset.loc[self.dataset['iso_code'] == iso_code, 'continent'].iloc[0]
    
    def getEntityISOCodesFromContinentISOCode(self, iso_code):
        continent = self.getContinentNameFromISOCode(iso_code)

        return self.dataset.loc[self.dataset['continent'] == continent, 'iso_code'].tolist()
        
    def getPopulationFromISOCode(self, iso_code):
        return self.dataset.loc[self.dataset['iso_code'] == iso_code, 'population'].iloc[0]
    
    def getContinentList(self):
        return [('Africa', 'AF'), 
                ('North America', 'NA'),
                ('South America', 'SA'),
                ('Asia', 'AS'), 
                ('Enrope', 'EU'), 
                ('Oceania', 'OC')]