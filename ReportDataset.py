import pandas as pd
import numpy as np
from Dataset import Dataset


class ReportDataset(Dataset):
    def prepare(self):
        cases_and_deaths = self.datasets['cases_and_deaths'].dataset.groupby(['iso_code']) \
                                                               .agg({'entity': 'last', 'cumulative_cases': 'last', 'cumulative_deaths': 'last'})
        cases_and_deaths = pd.merge(left=cases_and_deaths, 
                                    right=datasets['countries'].dataset.loc[:, ['iso_code', 'population']], 
                                    on=['iso_code'], 
                                    how="left").drop('iso_code', axis='columns').sort_values(by=['cumulative_cases', 'entity'], ascending=False)

        #cases_and_deaths.index = np.arange(1, len(cases_and_deaths.index) + 1)
        #cases_and_deaths.index.names = ['rank']

        cases_and_deaths['% of cases over population'] = round(cases_and_deaths['cumulative_cases'] / cases_and_deaths['population'] * 100, 2)
        cases_and_deaths['% of deaths over population'] = round(cases_and_deaths['cumulative_deaths'] / cases_and_deaths['population'] * 100, 2)
        cases_and_deaths['% of deaths over cases'] = round(cases_and_deaths['cumulative_deaths'] / cases_and_deaths['cumulative_cases'] * 100, 2)
