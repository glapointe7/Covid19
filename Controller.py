from CountriesModel import CountriesModel
from VaccinationsModel import VaccinationsModel
from CasesAndDeathsModel import CasesAndDeathsModel
from TestsModel import TestsModel
from HospitalizationsModel import HospitalizationsModel


class Controller:
    def __init__(self):
        self.countries_model = CountriesModel()
        self.vaccinations_model = VaccinationsModel()
        self.cases_and_deaths_model = CasesAndDeathsModel()
        self.tests_model = TestsModel()
        self.hospitalizations_model = HospitalizationsModel()
