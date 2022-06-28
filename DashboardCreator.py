from CasesAndDeathsDashboardBuilder import CasesAndDeathsDashboardBuilder
from VaccinationsDashboardBuilder import VaccinationsDashboardBuilder
from TestsDashboardBuilder import TestsDashboardBuilder
from HospitalizationsDashboardBuilder import HospitalizationsDashboardBuilder
from SummaryDashboardBuilder import SummaryDashboardBuilder
from StringencyDashboardBuilder import StringencyDashboardBuilder


class DashboardCreator:
    def __init__(self):
        self.builder = None
    
    def setBuilder(self, dashboard_selected, datasets):
        builder = {}
        if len(datasets['summary']) > 0:
            builder['Summary'] = SummaryDashboardBuilder(datasets['summary'])
        if len(datasets['stringency']) > 0:
            builder['Stringency'] = StringencyDashboardBuilder(datasets['stringency'])
        if len(datasets['cases_and_deaths']) > 0:
            builder['Cases and deaths'] = CasesAndDeathsDashboardBuilder(datasets['cases_and_deaths'])
        if len(datasets['vaccinations']) > 0:
            vaccinations = {'general': datasets['vaccinations']}
            if len(datasets['vaccinations_by_age']) > 0:
                vaccinations['by_age'] = datasets['vaccinations_by_age']
            if len(datasets['vaccinations_by_manufacturer']) > 0:
                vaccinations['by_manufacturer'] = datasets['vaccinations_by_manufacturer']
            builder['Vaccinations'] = VaccinationsDashboardBuilder(vaccinations)
        if len(datasets['tests']) > 0:
            builder['Tests'] = TestsDashboardBuilder(datasets['tests'])
        if len(datasets['hospitalizations']) > 0:
            builder['Hospitalizations'] = HospitalizationsDashboardBuilder(datasets['hospitalizations'])
        
        if dashboard_selected in builder.keys():
            self.builder = builder.get(dashboard_selected)