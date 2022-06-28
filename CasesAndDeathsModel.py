import pandas as pd


class CasesAndDeathsModel:
    def __init__(self):
        self.cases_and_deaths = None

    def downloadCasesDataset(self):
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
        self.cases_and_deaths = pd.read_csv(url)
                                     
        self.vaccinations = self.vaccinations.rename({'location': 'entity'}, axis='columns') \
                                             .drop(['daily_vaccinations_raw', 'daily_vaccinations_per_million'], axis='columns') \
                                             .sort_values(by=['entity', 'date'], ascending=True)
