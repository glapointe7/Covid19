import pandas as pd
import numpy as np
from Dataset import Dataset

class StatsDataset(Dataset):
    def prepare(self, datasets):
        self.dataset = datasets['cases_and_deaths'].dataset.groupby(['iso_code']) \
                                                   .agg({'cumulative_cases': 'last', 
                                                         'cumulative_deaths': 'last',
                                                         'new_cases': 'last',
                                                         'new_deaths': 'last',
                                                         'entity': 'last'
                                                   })
        self.dataset = pd.merge(left=self.dataset,
                                right=datasets['countries'].dataset[['iso_code', 'poverty_%', 'density', 'population', 'continent']],
                                on=['iso_code'],
                                how='left')
        self.dataset['cases_over_pop_%'] = self.dataset['cumulative_cases'] / self.dataset['population'] * 100
        self.dataset['deaths_over_pop_%'] = self.dataset['cumulative_deaths'] / self.dataset['population'] * 100
        self.dataset['deaths_over_cases_%'] = self.dataset['cumulative_deaths'] / self.dataset['cumulative_cases'] * 100
        
        cumulative_cases = self.dataset['cumulative_cases'].astype(float)
        self.dataset['cumulative_cases_log'] = np.log(cumulative_cases, 
                                                      out=np.zeros_like(cumulative_cases), 
                                                      where=(cumulative_cases != 0))
        cumulative_deaths = self.dataset['cumulative_deaths'].astype(float)
        self.dataset['cumulative_deaths_log'] = np.log(cumulative_deaths, 
                                                       out=np.zeros_like(cumulative_deaths), 
                                                       where=(cumulative_deaths != 0))
        

        percentage_vaccinations = datasets['vaccinations'].dataset.groupby(['iso_code']) \
                                                                  .agg({'people_1st_dose_%': 'last'})
        self.dataset = pd.merge(left=self.dataset,
                                right=percentage_vaccinations,
                                how="left",
                                on=['iso_code'])
                                
    def correlationMatrix(self):
        columns_to_drop = ['entity', 'iso_code', 'population', 'deaths_over_cases_%', 'cumulative_cases_log', 'cumulative_deaths_log', 
                           'continent']
        return self.dataset.drop(columns_to_drop, axis='columns') \
                           .corr().style.background_gradient(cmap='coolwarm').format('{:.2f}')
        
    def extractOutliers(self):
        percentile = self.dataset['deaths_over_cases_%'].describe()
        IQR = percentile['75%'] - percentile['25%']
        threshold = percentile['75%'] + 1.5 * IQR
        
        return self.dataset.loc[self.dataset['deaths_over_cases_%'] >= threshold, ['entity', 'deaths_over_cases_%']] \
                           .sort_values(by=['deaths_over_cases_%'], ascending=False)
    
    '''
    Functions returning percentages.
    '''
    def europeFirstDoseAgainstCasesOverPopulation(self):
        countries = self.dataset.loc[self.dataset['continent'] == 'Europe', ['people_1st_dose_%', 'cases_over_pop_%', 'iso_code']]
        constraints = countries.loc[(countries['people_1st_dose_%'] >= 50) & (countries['cases_over_pop_%'] >= 20), 'iso_code']
        
        return len(constraints) / len(countries) * 100
        
    def africaFirstDoseAgainstCasesOverPopulation(self):
        countries = self.dataset.loc[self.dataset['continent'] == 'Africa', ['people_1st_dose_%', 'cases_over_pop_%', 'iso_code']]
        constraints = countries.loc[(countries['people_1st_dose_%'] < 50) & (countries['cases_over_pop_%'] < 2), 'iso_code']
        
        return len(constraints) / len(countries) * 100
        
    def firstDoseAgainstPoverty(self):
        countries = self.dataset.loc[self.dataset['continent'] == 'Africa', ['people_1st_dose_%', 'poverty_%', 'iso_code']]
        constraints = countries.loc[(countries['people_1st_dose_%'] < 50) & (countries['poverty_%'] >= 6), 'iso_code']
        
        return len(constraints) / len(countries) * 100
        
    def deathsOverPopulationAgainstPoverty(self):
        countries = self.dataset.loc[self.dataset['continent'] == 'Africa', ['deaths_over_pop_%', 'poverty_%', 'iso_code']]
        constraints = countries.loc[(countries['deaths_over_pop_%'] < 0.05) & (countries['poverty_%'] >= 6), 'iso_code']
        
        return len(constraints) / len(countries) * 100
        
    def casesOverPopulationAgainstPoverty(self):
        countries = self.dataset.loc[self.dataset['continent'] == 'Africa', ['cases_over_pop_%', 'poverty_%', 'iso_code']]
        constraints = countries.loc[(countries['cases_over_pop_%'] < 2) & (countries['poverty_%'] >= 6), 'iso_code']
        
        return len(constraints) / len(countries) * 100