import CountriesModel


class DatasetController:
    def __init__(self):
        self.countries_model = CountriesModel()
        
    def prepareCountriesDataset(self):
        self.countries_model.downloadCountriesDataset()
        self.countries_model.addPopulationFeature()
        self.countries_model.addPovertyFeature()
        self.countries_model.addDensityFeature(year=2020)
