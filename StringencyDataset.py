import pandas as pd
import numpy as np
from Dataset import Dataset

class StringencyDataset(Dataset):
    '''
    SELECT CountryName AS entity, CountryCode AS iso_code, Date AS date, StringencyIndex AS stringency_index, GovernmentResponseIndex AS government_response_index
    FROM Stringency
    '''
    def prepare(self):
        url = "https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv"
        columns = {'CountryName': 'entity', 'CountryCode': 'iso_code', 'Date': 'date', 'StringencyIndex': 'stringency_index', 
                   'GovernmentResponseIndex': 'government_response_index'}
        self.dataset = pd.read_csv(url,  usecols=columns.keys()).fillna(0).rename(columns=columns)
        self.dataset['date'] = pd.to_datetime(self.dataset['date'], format="%Y%m%d").dt.strftime('%Y-%m-%d')
        self.dataset = self.dataset.groupby(['iso_code', 'date']) \
                                   .agg({'entity': 'last',
                                         'stringency_index': 'last',
                                         'government_response_index': 'last'}) \
                                   .reset_index()