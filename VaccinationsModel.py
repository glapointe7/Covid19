import pandas as pd


class VaccinationsModel:
    def __init__(self):
        self.vaccinations = None

    def downloadVaccinationsDataset(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
        self.vaccinations = pd.read_csv(url)
                                     
        self.vaccinations = self.vaccinations.rename({'location': 'entity'}, axis='columns') \
                                             .drop(['daily_vaccinations_raw', 'daily_vaccinations_per_million'], axis='columns')
                                             .sort_values(by=['entity', 'date'], ascending=True)
