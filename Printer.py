import matplotlib.pyplot as plt

import CasesDeathsPreparator
import CasesAndDeathsPrinter
import VaccinationsPrinter
import HospitalizationsPrinter

def plotVaccinationsByRegion(vaccination, region):
    region_vaccination = VaccinationsPrinter.getVaccinationsByRegion(vaccination, region)
    region_vaccination = region_vaccination.set_index('date')

    fig, axes = plt.subplots(3, 2, figsize=(25, 20))
    VaccinationsPrinter.plotCumulativeVaccinationsPieChart(region_vaccination.iloc[[-1]], axes[0, 0])
    VaccinationsPrinter.plotCumulativeDosesBarChart(region_vaccination.iloc[[-1]], axes[0, 1], fig)
    VaccinationsPrinter.plotCumulativeVaccinations(region_vaccination['total_vaccinations'], axes[1, 0])
    VaccinationsPrinter.plotNewVaccinations(region_vaccination['daily_vaccinations'], axes[1, 1])
    VaccinationsPrinter.plotCumulativeVaccinationsByDose(region_vaccination, axes[2, 0])
    VaccinationsPrinter.plotNewFirstDoseVaccinations(region_vaccination['daily_people_1st_dose'], axes[2, 1])
    plt.subplots_adjust(wspace=0.5, hspace=0.4)
    plt.show()

def plotHospitalizationsByRegion(hospitalizations, region):
    daily_hospitalizations = hospitalizations.loc[hospitalizations['entity'] == region, hospitalizations.columns != 'entity']
    daily_hospitalizations = daily_hospitalizations.groupby(['date', 'indicator'])['value'].first().unstack()

    fig, axes = plt.subplots(1, 2, figsize=(20, 7))
    HospitalizationsPrinter.plotDailyHospitalizations(daily_hospitalizations, axes[0])

    columns = daily_hospitalizations.columns.to_list()
    columns = list(filter(lambda column: column.endswith('million'), columns))
    if len(columns) > 0:
        HospitalizationsPrinter.plotHospitalizationsPerMillionBarChart(daily_hospitalizations[columns].iloc[-1], axes[1])
    plt.subplots_adjust(wspace=0.6)
    plt.show()

def plotVaccinationsByManufacturerByRegion(vaccinations_by_manufacturer, region):
    weekly_vaccinations = vaccinations_by_manufacturer.loc[vaccinations_by_manufacturer['entity'] == region, vaccinations_by_manufacturer.columns != 'entity']

    fig, axes = plt.subplots(1, 2, figsize=(20, 7))
    VaccinationsPrinter.plotWeeklyVaccinationsByManufacturer(weekly_vaccinations, axes[0])
    VaccinationsPrinter.plotCumulativeVaccinationsByManufacturerBarChart(weekly_vaccinations, axes[1], fig)
    plt.subplots_adjust(wspace=0.5)
    plt.show()

def plotAccelerations(dataset):
    fig, axes = plt.subplots(2, 2, figsize=(25, 15))
    CasesAndDeathsPrinter.plotAccelerationNormalDistribution(dataset['deaths_acceleration'], 'Deaths', axes[0, 0])
    CasesAndDeathsPrinter.plotAccelerationNormalDistribution(dataset['cases_acceleration'], 'Cases', axes[0, 1])
    CasesAndDeathsPrinter.plotAccelerationData(dataset['deaths_acceleration'], 'Deaths', axes[1, 0])
    CasesAndDeathsPrinter.plotAccelerationData(dataset['cases_acceleration'], 'Cases', axes[1, 1])
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    plt.show()