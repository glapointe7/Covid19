import pandas as pd
from Dataset import Dataset

class VaccinationsByAgeDataset(Dataset):
    '''
    SELECT location AS entity, date, age_group, people_vaccinated_per_hundred AS people_1st_dose_percent,
           people_fully_vaccinated_per_hundred AS people_2nd_dose_percent, people_with_booster_per_hundred AS people_3rd_dose_percent
    FROM VaccinationsByAgeGroup
    ORDER BY entity, date ASC
    '''
    def prepare(self, countries):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-age-group.csv"
        self.dataset = pd.read_csv(url)
        
        new_column_names = {
            'location': 'entity', 'people_vaccinated_per_hundred': 'people_1st_dose_%',
            'people_fully_vaccinated_per_hundred': 'people_2nd_dose_%', 'total_boosters_per_hundred': 'people_3rd_dose_%'
        }
        
        self.dataset = self.dataset.rename(new_column_names, axis='columns')
        self.dataset = pd.merge(left=self.dataset, 
                                right=countries.dataset.loc[:, ['entity', 'iso_code']], 
                                on=['entity'], 
                                how="left")
        self.dataset = self.dataset.sort_values(by=['entity', 'date'], ascending=True)
                                   
                