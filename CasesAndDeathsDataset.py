import pandas as pd
import numpy as np
from Dataset import Dataset

class CasesAndDeathsDataset(Dataset):
    '''
    SELECT Province/State AS province_or_state, Country/Region AS entity, Lat AS latitude, Long AS longitude, date, cumulative_cases
    FROM (
        SELECT 1/22/20 as date FROM Cases
        UNION ALL
        SELECT 1/23/20 as date FROM Cases
        UNION ALL
        ...
        UNION ALL
        SELECT 3/25/22 as date FROM Cases
        # New dates to be appended with "union all" as the table is updated with new dates.
    ) AS Cases
    '''
    def queryCasesDataset(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/scripts/input/jhu/time_series_covid19_confirmed_global.csv"
        cases = pd.read_csv(url).fillna("")
        
        # Each date column are transformed to a row for each country and province or state.
        new_column_names = {'Province/State': 'province_or_state', 'Country/Region': 'entity', 'Lat': 'latitude', 'Long': 'longitude'}
        return cases.rename(new_column_names, axis='columns') \
                    .melt(['province_or_state', 'entity', 'latitude', 'longitude'], var_name='date', value_name='cumulative_cases')


    '''
    SELECT Province/State AS province_or_state, Country/Region AS entity, Lat AS latitude, Long AS longitude, date, cumulative_deaths
    FROM (
        SELECT 1/22/20 as date FROM Deaths
        UNION ALL
        SELECT 1/23/20 as date FROM Deaths
        UNION ALL
        ...
        UNION ALL
        SELECT 3/25/22 as date FROM Deaths
        # New dates to be appended with "union all" as the table is updated with new dates.
    ) AS Deaths
    '''
    def queryDeathsDataset(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/scripts/input/jhu/time_series_covid19_deaths_global.csv"
        deaths = pd.read_csv(url).fillna("")
        
        # Each date column are transformed to a row for each country and province or state. 
        new_column_names = {'Province/State': 'province_or_state', 'Country/Region': 'entity', 'Lat': 'latitude', 'Long': 'longitude'}
        return deaths.rename(new_column_names, axis='columns') \
                     .melt(['province_or_state', 'entity', 'latitude', 'longitude'], var_name='date', value_name='cumulative_deaths')
    
    def adjustCountryNames(self):
        wrong_country_names = ['West Bank and Gaza', 'Congo (Kinshasa)', 'Taiwan*', 
                               'Korea, South', 'US', 'Burma', 'Congo (Brazzaville)']
        true_country_names = ['Palestine', 'Democratic Republic of Congo', 
                              'Taiwan', 'South Korea', 'United States', 'Myanmar', 'Congo']
        for i, name in enumerate(wrong_country_names):
            self.dataset.loc[self.dataset['entity'] == name, 'entity'] = true_country_names[i]
    
    '''
    SELECT C.province_or_state, C.entity, DATE_FORMAT(C.date, '%Y-%m-%d') AS date, C.latitude, C.longitude, C.cumulative_cases, 
           D.cumulative_deaths, P.iso_code
    FROM Cases AS C
        INNER JOIN Deaths AS D ON (C.province_or_state = D.province_or_state, 
                                   C.entity = D.entity, 
                                   C.latitude = D.latitude,
                                   C.longitude = D.longitude,
                                   C.date = D.date)
        LEFT JOIN Countries AS P ON (C.entity = P.entity)
    ORDER BY C.province_or_state, C.entity, date ASC
    '''
    def prepare(self, countries):
        cases = self.queryCasesDataset()
        deaths = self.queryDeathsDataset()
        self.dataset = pd.merge(left=cases, 
                                right=deaths, 
                                on=['province_or_state', 'entity', 'latitude', 'longitude', 'date'], 
                                how="inner")
                                
        self.adjustCountryNames()
        self.repairLatitudeAndLongitude('Ontario', "Repatriated Travellers")
        self.repairLatitudeAndLongitude('Beijing', 'Unknown')
        
        self.dataset = self.dataset.groupby(['entity', 'date']) \
                                   .agg({'latitude': 'last',
                                         'longitude': 'last',
                                         'cumulative_cases': 'sum', 
                                         'cumulative_deaths': 'sum'}) \
                                   .reset_index()
    
        self.dataset = pd.merge(left=self.dataset, 
                                right=countries.dataset.loc[:, ['entity', 'iso_code']], 
                                on=['entity'], 
                                how="left")
        
        # ISO code of Antarctica was NA, so we assign it to 'AN'.
        self.dataset.loc[self.dataset['entity'] == 'Antarctica', 'iso_code'] = 'AN'
        
        self.dataset['date'] = pd.to_datetime(self.dataset['date'], format="%m/%d/%y").dt.strftime('%Y-%m-%d')
        self.dataset = self.dataset.sort_values(by=['entity', 'date'], ascending=True)
        self.dataset['deaths_over_cases_%'] = self.dataset['cumulative_deaths'] / self.dataset['cumulative_cases'] * 100
        
        self.dataset['new_cases'] = self.dataset.groupby(['entity'])['cumulative_cases'].diff().fillna(0)
        self.dataset['new_deaths'] = self.dataset.groupby(['entity'])['cumulative_deaths'].diff().fillna(0)
    
    def repairLatitudeAndLongitude(self, good_state, bad_state):
        latitude = self.dataset.loc[self.dataset['province_or_state'] == good_state, 'latitude'].iloc[0]
        longitude = self.dataset.loc[self.dataset['province_or_state'] == good_state, 'latitude'].iloc[0]
        self.dataset.loc[self.dataset['province_or_state'] == bad_state, 'latitude'] = latitude
        self.dataset.loc[self.dataset['province_or_state'] == bad_state, 'longitude'] = longitude
    
    def extractFromISOCode(self, iso_code):
        return self.dataset.loc[self.dataset['iso_code'] == iso_code].set_index('date')
        
    def getFirstCasesDate(self):
        return self.dataset.loc[self.dataset['cumulative_cases'] > 0, 'date'].iloc[0]