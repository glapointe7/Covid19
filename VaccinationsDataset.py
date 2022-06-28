import pandas as pd
from Dataset import Dataset

class VaccinationsDataset(Dataset):
    '''
    SELECT location AS entity, iso_code, date, total_vaccinations AS cumulative_vaccines, people_vaccinated AS people_1st_dose, 
           people_fully_vaccinated AS people_2nd_dose, total_boosters AS people_3rd_dose, daily_vaccinations AS new_vaccines,
           total_vaccinations_per_hundred AS cumulative_vaccines_percent, people_vaccinated_per_hundred AS people_1st_dose_percent,
           people_fully_vaccinated_per_hundred AS people_2nd_dose_percent, total_boosters_per_hundred AS people_3rd_dose_percent,
           daily_people_vaccinated AS new_people_1st_dose, daily_people_vaccinated_per_hundred AS new_people_1st_dose_percent
    FROM Vaccinations
    ORDER BY entity, date ASC
    '''
    def prepare(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
        self.dataset = pd.read_csv(url).fillna(method='ffill')
        
        new_column_names = {
            'location': 'entity', 'total_vaccinations': 'cumulative_vaccines', 'people_vaccinated': 'people_1st_dose',
            'people_fully_vaccinated': 'people_2nd_dose', 'total_boosters': 'people_3rd_dose', 'daily_vaccinations': 'new_vaccines',
            'total_vaccinations_per_hundred': 'cumulative_vaccines_%', 'people_vaccinated_per_hundred': 'people_1st_dose_%',
            'people_fully_vaccinated_per_hundred': 'people_2nd_dose_%', 'total_boosters_per_hundred': 'people_3rd_dose_%',
            'daily_people_vaccinated': 'new_people_1st_dose', 'daily_people_vaccinated_per_hundred': 'new_people_1st_dose_%'
        }
        
        # OWID iso codes to rename  
        iso_codes_owid = {
            'OWID_AFR': 'AF',
            'OWID_ASI': 'AS',
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
            'OWID_WRL': 'WR'
        }
        self.dataset['iso_code'] = self.dataset['iso_code'].replace(iso_codes_owid)
        
        self.dataset = self.dataset.rename(new_column_names, axis='columns') \
                                   .drop(['daily_vaccinations_raw', 'daily_vaccinations_per_million'], axis='columns') \
                                   .sort_values(by=['entity', 'date'], ascending=True)