import pandas as pd
from Dataset import Dataset


class WorldDataset(Dataset):
    def prepare(self, datasets):
        self.dataset = datasets['cases_and_deaths'].dataset.groupby(['date']) \
                                                   .agg({'cumulative_cases': 'sum', 
                                                         'cumulative_deaths': 'sum',
                                                         'new_cases': 'sum',
                                                         'new_deaths': 'sum'}) \
                                                   .reset_index()