import pandas as pd
import numpy as np
from Dataset import Dataset


class TestsDataset(Dataset):
    def prepare(self, countries, cases_and_deaths):
        # Remove the divide by 0 warning because we already manage by replacing infinity by 0.
        np.seterr(divide='ignore', invalid='ignore')
        
        self.dataset = self.queryTestsDataset()
        
        iso_codes = set(self.dataset['iso_code'])
        for iso_code in iso_codes:
            tests = self.dataset.loc[self.dataset['iso_code'] == iso_code].copy()
            tests['cumulative_tests_over_population_%'] = round(tests['cumulative_total'] * 100 / countries.dataset.loc[countries.dataset['iso_code'] == iso_code, 'population'].iloc[0], 6)
            
            ## If the ISO code in the tests dataset is not in the cases and deaths dataset. 
            cases_entity = cases_and_deaths.dataset.loc[cases_and_deaths.dataset['iso_code'] == iso_code].copy()
            if len(cases_entity) > 0:
                # If tests data started to be entered before the count of cases which should not have occured.
                start_date = max(tests['date'].min(), cases_entity['date'].min())
                end_date = min(tests['date'].max(), cases_entity['date'].max())
                mask_cases = (cases_entity['date'] >= start_date) & (cases_entity['date'] <= end_date)
                
                mask = (tests['date'] >= start_date) & (tests['date'] <= end_date)
                rolling_cases = np.array(cases_entity.loc[mask_cases, 'new_cases'].rolling(7).mean())
                rolling_tests = np.array(tests.loc[mask, 'new_tests'].rolling(7).mean())
                tests.loc[mask, 'positive_test_rate'] = rolling_cases / rolling_tests
                tests.loc[mask, 'positive_test_rate'] = tests.loc[mask, 'positive_test_rate'].replace([np.inf, -np.inf], [0, 0]).fillna(0).round(6)
                
                tests.loc[:, 'tests_per_cases'] = 1 / tests['positive_test_rate']
                tests.loc[:, 'tests_per_cases'] = tests['tests_per_cases'].replace([np.inf, -np.inf], [0, 0]).round(2)
            
            self.dataset.loc[self.dataset['iso_code'] == iso_code] = tests
    
    '''
    SELECT REGEXP_REPLACE(Entity, ' - .*$', '') AS entity, REGEXP_REPLACE("ISO code", 'OWID_', '') AS iso_code, 
           Date as date, "Cumulative total" AS cumulative_total
    FROM Tests;
    
    ALTER TABLE Tests
        ADD COLUMN new_tests INT NOT NULL
        ADD COLUMN cumulative_tests_over_population_percent DECIMAL(12,6) NOT NULL
        ADD COLUMN positive_test_rate DECIMAL(8,6)
        ADD COLUMN tests_per_cases DECIMAL(8,2)
    '''
    def queryTestsDataset(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/testing/covid-testing-all-observations.csv"
        new_column_names = {'Entity': 'entity', 'ISO code': 'iso_code', 'Date': 'date', 'Cumulative total': 'cumulative_total'}
        tests = pd.read_csv(url, 
                            usecols=list(new_column_names.keys()))
        tests = tests.rename(new_column_names, axis='columns')
        tests['iso_code'] = tests['iso_code'].replace(regex=r'^OWID_', value='')
        tests['entity'] = tests['entity'].replace(regex=r' - .*$', value='')
        tests['date'] = pd.to_datetime(tests['date'], format="%Y-%m-%d").dt.strftime('%Y-%m-%d')
        tests['cumulative_total'] = tests.groupby(['iso_code'])['cumulative_total'].fillna(method='ffill')
        
        # Add 4 new columns.
        tests['new_tests'] = tests.groupby(['iso_code'])['cumulative_total'].diff().fillna(0)
        tests['cumulative_tests_over_population_%'] = 0
        tests['positive_test_rate'] = np.nan
        tests['tests_per_cases'] = np.nan
        
        return tests