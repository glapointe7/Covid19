import pandas as pd
import numpy as np
from Dataset import Dataset


class SummaryDataset(Dataset):
    def prepare(self, datasets):
        self.dataset = datasets['cases_and_deaths'].dataset.groupby(['iso_code']) \
                                                   .agg({'cumulative_cases': 'last', 
                                                         'cumulative_deaths': 'last',
                                                         'new_cases': 'last',
                                                         'new_deaths': 'last',
                                                         'latitude': 'first',
                                                         'longitude': 'first',
                                                         'entity': 'last'}) \
                                                   .reset_index()
        self.dataset = pd.merge(left=self.dataset,
                                right=datasets['countries'].dataset.loc[:, ['iso_code', 'population', 'continent']],
                                on=['iso_code'],
                                how='left')
        self.dataset['cases_over_pop_%'] = round(self.dataset['cumulative_cases'] / self.dataset['population'] * 100, 2)
        self.dataset['deaths_over_pop_%'] = round(self.dataset['cumulative_deaths'] / self.dataset['population'] * 100, 2)
        self.dataset['deaths_over_cases_%'] = round(self.dataset['cumulative_deaths'] / self.dataset['cumulative_cases'] * 100, 2)
        vaccinations = datasets['vaccinations'].dataset.groupby(['iso_code']) \
                                                       .agg({'people_2nd_dose_%': 'last'}) \
                                                       .reset_index()
        self.dataset = pd.merge(left=self.dataset,
                                right=vaccinations,
                                on=['iso_code'],
                                how='left')
    
    def prepareContinentOrWorld(self, iso_code, datasets):
        cases_and_deaths = datasets['cases_and_deaths'].dataset
        if iso_code != 'WR':
            iso_codes = datasets['countries'].getEntityISOCodesFromContinentISOCode(iso_code)
            cases_and_deaths = cases_and_deaths.query("iso_code in @iso_codes")
        dataset = cases_and_deaths.groupby(['date']) \
                                  .agg({'cumulative_cases': 'sum', 
                                        'cumulative_deaths': 'sum',
                                        'new_cases': 'sum',
                                        'new_deaths': 'sum'}) \
                                  .reset_index().tail(1)
        dataset['population'] = datasets['countries'].getPopulationFromISOCode(iso_code)
        dataset['cases_over_pop_%'] = dataset['cumulative_cases'] / dataset['population'] * 100
        
        dataset['people_2nd_dose_%'] = datasets['vaccinations'].dataset.loc[datasets['vaccinations'].dataset['iso_code'] == iso_code, 'people_2nd_dose_%'].iloc[-1]
        
        return dataset
        
    def topCountriesOn(self, feature, top_n):
        return self.dataset[['entity', feature]] \
                           .sort_values(by=[feature], ascending=False) \
                           .head(top_n) \
                           .set_index('entity')