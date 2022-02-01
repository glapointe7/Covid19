import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd


def getVaccinationsByRegion(dataset, region):
    daily_vaccinations = dataset.loc[dataset['entity'] == region]
    daily_vaccinations = daily_vaccinations.drop(['entity', 'iso_code'], axis=1)
    daily_vaccinations.set_axis(labels=['date', 'total_vaccinations', 'people_1st_dose', 'people_2nd_dose', 'people_3rd_dose', 'daily_vaccinations', 
                                       '%_total_vaccinations', '%_people_1st_dose', '%_people_2nd_dose', '%_people_3rd_dose', 'daily_people_1st_dose', '%_daily_people_1st_dose'], 
                                    axis=1, 
                                    inplace=True)
    return daily_vaccinations

def plotCumulativeVaccinations(daily_vaccinations):
    ax = daily_vaccinations['total_vaccinations'].plot(label="Total Vaccinations")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of vaccins', fontsize=16)
    plt.title("Cumulative number of vaccins administrated", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotNewVaccinations(daily_vaccinations):
    ax = daily_vaccinations['daily_vaccinations'].plot(label="Daily Total Vaccinations")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of vaccins', fontsize=16)
    plt.title("Number of new daily vaccins administrated", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotCumulativeVaccinationsByDose(daily_vaccinations):
    ax = daily_vaccinations['people_1st_dose'].plot(label="People with 1st Dose")
    daily_vaccinations['people_2nd_dose'].plot(label="People with 2nd Dose")
    daily_vaccinations['people_3rd_dose'].plot(label="People with 3rd Dose")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of vaccins', fontsize=16)
    plt.title("Cumulative number of 1st, 2nd and 3rd doses administrated", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.legend()

def plotNewFirstDoseVaccinations(daily_vaccinations):
    ax = daily_vaccinations['daily_people_1st_dose'].astype(np.int64).plot(label="People with 1st Dose")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of vaccins', fontsize=16)
    plt.title("Number of new daily first doses administrated", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
def plotCumulativeDosesBarChart(dataset, axe, fig):
    vaccins = pd.DataFrame({'doses': ["Total vaccins", "Total 1st dose", "Total 2nd dose", "Total 3rd dose"], 
                            'number_of_vaccins': [dataset['total_vaccinations'].iloc[0], dataset['people_1st_dose'].iloc[0],
                                                  dataset['people_2nd_dose'].iloc[0], dataset['people_3rd_dose'].iloc[0]]})

    ax = vaccins.set_index('doses').plot(kind='barh', legend=False, ax=axe)
    plt.xlabel('People vaccinated', fontsize=16)
    plt.title("Number of people vaccinated by number of doses", fontsize=20)
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    widths = []
    r = fig.canvas.get_renderer()
    for i, value in enumerate(vaccins['number_of_vaccins']):
        t = ax.text(value / 3, i, str(value), color='black', fontsize=14)
        # Transform the coordinates to obtain the value coordinates instead.
        widths.append(t.get_window_extent(renderer=r).transformed(plt.gca().transData.inverted()).width)

    percentages = [dataset['%_total_vaccinations'].iloc[0], dataset['%_people_1st_dose'].iloc[0], 
                   dataset['%_people_2nd_dose'].iloc[0], dataset['%_people_3rd_dose'].iloc[0]]
    for i, value in enumerate(percentages):
        ax.text(vaccins['number_of_vaccins'][i] / 3 + 1.2 * widths[i], i, " [" + str(value) + " %]", color='darkorange', fontsize=14)

def plotCumulativeVaccinationsPieChart(dataset):
    vaccination_percentage = {"Not Vaccinated": 100.0 - float(dataset['%_people_1st_dose'].iloc[0]),
                              "1st Dose Only": float(dataset['%_people_1st_dose'].iloc[0]) - float(dataset['%_people_2nd_dose'].iloc[0]),
                              "1st and 2nd Doses": float(dataset['%_people_2nd_dose'].iloc[0]) - float(dataset['%_people_3rd_dose'].iloc[0]),
                              "All 3 Doses": float(dataset['%_people_3rd_dose'].iloc[0])}
   
    plt.pie(x=list(vaccination_percentage.values()), 
            labels=vaccination_percentage.keys(), 
            autopct='%1.1f%%', 
            textprops={'fontsize': 14},
            shadow=True)
    plt.title("Percentage of people having their 1st dose only, 2nd dose and booster dose", fontsize=20)
    
def plotWeeklyVaccinationsByManufacturer(weekly_vaccinations, axe):
    weekly_vaccinations.set_index('date') \
                       .groupby('vaccine')['total_vaccinations'] \
                       .plot(legend=True, ax=axe)

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of vaccinations', fontsize=16)
    plt.title("Number of weekly people vaccinated by vaccine manufacturer", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    axe.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
def plotCumulativeVaccinationsByManufacturerBarChart(weekly_vaccinations, fig, axe):
    indices = weekly_vaccinations.groupby(['vaccine']).date.transform(max) == weekly_vaccinations['date']
    weekly_vaccinations_summary = weekly_vaccinations[indices]
    print("Latest date updated: " + weekly_vaccinations_summary['date'].iloc[0])
    weekly_vaccinations_summary = weekly_vaccinations_summary.drop('date', axis=1)
    weekly_vaccinations_summary = weekly_vaccinations_summary.set_index('vaccine')
    
    weekly_vaccinations_summary.plot(kind='barh', legend=False, ax=axe)
    
    plt.ylabel('Manufacturer', fontsize=16)
    plt.xlabel('People vaccinated', fontsize=16)
    plt.tick_params(axis='x', rotation=90)
    plt.title("Total number of people vaccinated by vaccine manufacturer", fontsize=20)
    axe.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    widths = []
    r = fig.canvas.get_renderer()
    for i, value in enumerate(weekly_vaccinations_summary['total_vaccinations']):
        t = axe.text(value / 3, i, str(value), color='black', fontsize=14)
        widths.append(t.get_window_extent(renderer=r).transformed(plt.gca().transData.inverted()).width)
    
    total_vaccinations = np.sum(weekly_vaccinations_summary['total_vaccinations'])
    percentages = round(weekly_vaccinations_summary['total_vaccinations'] / total_vaccinations * 100, 2)
    for i, value in enumerate(percentages):
        axe.text(weekly_vaccinations_summary['total_vaccinations'][i] / 3 + 1.2 * widths[i], i, " [" + str(value) + " %]", color='darkorange', fontsize=14)
        
def plotAgeGroupVaccinationsBarChart(weekly_vaccinations_age_group):
    indices = weekly_vaccinations_age_group.groupby(['age_group'])['date'].transform(max) == weekly_vaccinations_age_group['date']
    weekly_vaccinations_age_group_summary = weekly_vaccinations_age_group[indices]
    print("Latest date updated: " + weekly_vaccinations_age_group_summary['date'].iloc[0])
    weekly_vaccinations_age_group_summary = weekly_vaccinations_age_group_summary.drop('date', axis=1)
    weekly_vaccinations_age_group_summary = weekly_vaccinations_age_group_summary.set_index('age_group')
    
    plt.rcParams["figure.figsize"] = (15, 10)
    weekly_vaccinations_age_group_summary.plot(kind='bar')
    
    plt.xlabel('Age Groups', fontsize=16)
    plt.ylabel('Percentage of people', fontsize=16)
    plt.title("Percentage of people vaccinated grouped by age group", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    plt.show()