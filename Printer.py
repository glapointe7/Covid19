import matplotlib.pyplot as plt

import CasesDeathsPreparator
import CasesAndDeathsPrinter
import VaccinationsPrinter
import HospitalizationsPrinter

def plotVaccinationsByRegion(vaccination, region):
    region_vaccination = VaccinationsPrinter.getVaccinationsByRegion(vaccination, region)
    region_vaccination = region_vaccination.set_index('date')

    fig = plt.figure(figsize=(25, 20))
    ax1 = plt.subplot(3,2,1)
    VaccinationsPrinter.plotCumulativeVaccinationsPieChart(region_vaccination.iloc[[-1]])
    ax2 = plt.subplot(3,2,2)
    VaccinationsPrinter.plotCumulativeDosesBarChart(region_vaccination.iloc[[-1]], ax2, fig)
    ax3 = plt.subplot(3,2,3)
    VaccinationsPrinter.plotCumulativeVaccinations(region_vaccination)
    ax4 = plt.subplot(3,2,4)
    VaccinationsPrinter.plotNewVaccinations(region_vaccination)
    ax5 = plt.subplot(3,2,5)
    VaccinationsPrinter.plotCumulativeVaccinationsByDose(region_vaccination)
    ax6 = plt.subplot(3,2,6)
    VaccinationsPrinter.plotNewFirstDoseVaccinations(region_vaccination)
    plt.subplots_adjust(wspace=0.5, hspace=0.4)
    plt.show()

def plotHospitalizationsByRegion(hospitalizations, region):
    daily_hospitalizations = hospitalizations.loc[hospitalizations['entity'] == region, hospitalizations.columns != 'entity']
    daily_hospitalizations = daily_hospitalizations.groupby(['date', 'indicator'])['value'].first().unstack()

    plt.figure(figsize=(20, 7))
    ax1 = plt.subplot(1,2,1)
    HospitalizationsPrinter.plotDailyHospitalizations(daily_hospitalizations)

    columns = daily_hospitalizations.columns.to_list()
    columns = list(filter(lambda column: column.endswith('million'), columns))
    if len(columns) > 0:
        ax2 = plt.subplot(1,2,2)
        HospitalizationsPrinter.plotHospitalizationsPerMillionBarChart(daily_hospitalizations[columns].iloc[-1])
    plt.subplots_adjust(wspace=0.5)
    plt.show()

def plotVaccinationsByManufacturerByRegion(vaccinations_by_manufacturer, region):
    weekly_vaccinations = vaccinations_by_manufacturer.loc[vaccinations_by_manufacturer['entity'] == region, vaccinations_by_manufacturer.columns != 'entity']

    fig = plt.figure(figsize=(20, 7))
    ax1 = plt.subplot(1,2,1)
    VaccinationsPrinter.plotWeeklyVaccinationsByManufacturer(weekly_vaccinations, ax1)
    ax2 = plt.subplot(1,2,2)
    VaccinationsPrinter.plotCumulativeVaccinationsByManufacturerBarChart(weekly_vaccinations, fig, ax2)
    plt.subplots_adjust(wspace=0.5)
    plt.show()
