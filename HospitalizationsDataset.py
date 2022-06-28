import pandas as pd
from Dataset import Dataset

class HospitalizationsDataset(Dataset):
    '''
    SELECT entity, iso_code, date, indicator, value AS number_or_people
    FROM Hospitalizations
    ORDER BY entity, date ASC
    '''
    def prepare(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/hospitalizations/covid-hospitalizations.csv"
        self.dataset = pd.read_csv(url)
        
        new_column_names = {'value': 'number_of_people'}
        self.dataset = self.dataset.rename(new_column_names, axis='columns') \
                                   .sort_values(by=['entity', 'date'], ascending=True)