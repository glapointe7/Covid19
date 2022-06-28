import pandas as pd
from Dataset import Dataset

class VaccinationsByManufacturerDataset(Dataset):
    '''
    SELECT location AS entity, date, vaccine AS manufacturer, total_vaccinations AS cumulative_vaccines
    FROM VaccinationsByManufacturer
    ORDER BY entity, date ASC 
    '''
    def prepare(self, countries):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations-by-manufacturer.csv"
        self.dataset = pd.read_csv(url)
        
        new_column_names = {
            'location': 'entity', 'vaccine': 'manufacturer', 'total_vaccinations': 'cumulative_vaccines'
        }
        self.dataset = self.dataset.rename(new_column_names, axis='columns')
        
        self.dataset = pd.merge(left=self.dataset, 
                                right=countries.dataset.loc[:, ['entity', 'iso_code']], 
                                on=['entity'], 
                                how="left")
        self.dataset = self.dataset.sort_values(by=['entity', 'date'], ascending=True)
