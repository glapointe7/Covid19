import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def getVaccinationsByRegion(dataset, region):
    daily_vaccinations = dataset.loc[dataset['entity'] == region]
    daily_vaccinations = daily_vaccinations.drop(['entity', 'iso_code'], axis=1)
    daily_vaccinations.set_axis(labels=['date', 'total_vaccinations', 'people_1st_dose', 'people_2nd_dose', 'people_3rd_dose', 'daily_vaccinations', 
                                       '%_total_vaccinations', '%_people_1st_dose', '%_people_2nd_dose', '%_people_3rd_dose', 'daily_people_1st_dose', '%_daily_people_1st_dose'], 
                                    axis=1, 
                                    inplace=True)
    return daily_vaccinations

def plotCumulativeVaccinations(dataset, ax):
    dataset.plot(label="Total Vaccinations", ax=ax, rot=90)
    ax.set_xlabel('Date', fontdict={'fontsize': 16})
    ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 16})
    ax.set_title("Time series of the cumulative number of vaccins administrated", fontdict={'fontsize': 20})
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotNewVaccinations(dataset, ax):
    dataset.plot(label="Daily Total Vaccinations", ax=ax, rot=90)
    ax.set_xlabel('Date', fontdict={'fontsize': 16})
    ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 16})
    ax.set_title("Time series of the number of new vaccins administrated", fontdict={'fontsize': 20})
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotCumulativeVaccinationsByDose(dataset, ax):
    dataset['people_1st_dose'].plot(label="People with 1st Dose", ax=ax, rot=90, legend=True)
    dataset['people_2nd_dose'].plot(label="People with 2nd Dose", ax=ax, rot=90, legend=True)
    dataset['people_3rd_dose'].plot(label="People with 3rd Dose", ax=ax, rot=90, legend=True)

    ax.set_xlabel('Date', fontdict={'fontsize': 16})
    ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 16})
    ax.set_title("Time series of the cumulative number of 1st, 2nd and 3rd doses administrated", fontdict={'fontsize': 20})
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotNewFirstDoseVaccinations(dataset, ax):
    dataset.plot(label="People with 1st Dose", ax=ax, rot=90)
    ax.set_xlabel('Date', fontdict={'fontsize': 16})
    ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 16})
    ax.set_title("Time series of the number of new first doses administrated", fontdict={'fontsize': 20})
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
def plotCumulativeDosesBarChart(dataset, ax, fig):
    vaccins = pd.DataFrame({'doses': ["Total vaccins", "Total 1st dose", "Total 2nd dose", "Total 3rd dose"], 
                            'number_of_vaccins': [dataset['total_vaccinations'].iloc[0], dataset['people_1st_dose'].iloc[0],
                                                  dataset['people_2nd_dose'].iloc[0], dataset['people_3rd_dose'].iloc[0]]})

    vaccins.set_index('doses').plot.barh(ax=ax, legend=False)
    ax.set_xlabel('People vaccinated', fontdict={'fontsize': 16})
    ax.set_title("Number of people vaccinated by number of doses", fontdict={'fontsize': 20})
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    widths = []
    r = fig.canvas.get_renderer()
    for i, value in enumerate(vaccins['number_of_vaccins']):
        t = ax.text(value / 3, i, str(value), color='black', fontsize=14)
        # Transform the coordinates to obtain the value coordinates instead.
        widths.append(t.get_window_extent(renderer=r).transformed(ax.transData.inverted()).width)

    percentages = [dataset['%_total_vaccinations'].iloc[0], dataset['%_people_1st_dose'].iloc[0], 
                   dataset['%_people_2nd_dose'].iloc[0], dataset['%_people_3rd_dose'].iloc[0]]
    for i, value in enumerate(percentages):
        ax.text(vaccins['number_of_vaccins'][i] / 3 + 1.2 * widths[i], i, " [" + str(value) + " %]", color='darkorange', fontsize=14)

def plotCumulativeVaccinationsPieChart(dataset, ax):
    vaccination_percentage = {"Not Vaccinated": 100.0 - float(dataset['%_people_1st_dose'].iloc[0]),
                              "1st Dose Only": float(dataset['%_people_1st_dose'].iloc[0]) - float(dataset['%_people_2nd_dose'].iloc[0]),
                              "1st and 2nd Doses": float(dataset['%_people_2nd_dose'].iloc[0]) - float(dataset['%_people_3rd_dose'].iloc[0]),
                              "All 3 Doses": float(dataset['%_people_3rd_dose'].iloc[0])}
   
    ax.pie(x=list(vaccination_percentage.values()), 
           labels=vaccination_percentage.keys(), 
           autopct='%1.1f%%', 
           textprops={'fontsize': 14},
           shadow=True)
    ax.set_title("Percentage of people having their 1st dose only, 1st and 2nd doses only, and all doses", fontdict={'fontsize': 20})
    
####################################################################################################
    
def plotWeeklyVaccinationsByManufacturer(dataset, ax):
    dataset.set_index('date') \
           .groupby('vaccine')['total_vaccinations'] \
           .plot(legend=True, ax=ax, rot=90)

    ax.set_xlabel('Date', fontdict={'fontsize': 16})
    ax.set_ylabel('Number of vaccinations', fontdict={'fontsize': 16})
    ax.set_title("Number of weekly people vaccinated by vaccine manufacturer", fontdict={'fontsize': 20})
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
def plotCumulativeVaccinationsByManufacturerBarChart(dataset, ax, fig):
    indices = dataset.groupby(['vaccine']).date.transform(max) == dataset['date']
    weekly_vaccinations_summary = dataset[indices]
    print("Latest date updated: " + weekly_vaccinations_summary['date'].iloc[0])
    weekly_vaccinations_summary = weekly_vaccinations_summary.drop('date', axis=1)
    weekly_vaccinations_summary = weekly_vaccinations_summary.set_index('vaccine')
    
    weekly_vaccinations_summary.plot.barh(legend=False, ax=ax, rot=90)
    ax.set_xlabel('People vaccinated', fontdict={'fontsize': 16})
    ax.set_ylabel('Manufacturer', fontdict={'fontsize': 16})
    ax.set_title("Total number of people vaccinated by vaccine manufacturer", fontdict={'fontsize': 20})
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    widths = []
    r = fig.canvas.get_renderer()
    for i, value in enumerate(weekly_vaccinations_summary['total_vaccinations']):
        t = ax.text(x=value / 3, 
                    y=i, 
                    s=str(value), 
                    color='black', 
                    fontsize=14)
        widths.append(t.get_window_extent(renderer=r).transformed(ax.transData.inverted()).width)
    #transform=ax.get_xaxis_transform()
    
    total_vaccinations = np.sum(weekly_vaccinations_summary['total_vaccinations'])
    percentages = round(weekly_vaccinations_summary['total_vaccinations'] / total_vaccinations * 100, 2)
    for i, value in enumerate(percentages):
        ax.text(weekly_vaccinations_summary['total_vaccinations'][i] / 3 + 1.2 * widths[i], i, " [" + str(value) + " %]", color='darkorange', fontsize=14)
        
def plotAgeGroupVaccinationsBarChart(dataset):
    indices = dataset.groupby(['age_group'])['date'].transform(max) == dataset['date']
    weekly_vaccinations_age_group_summary = dataset[indices]
    print("Latest date updated: " + weekly_vaccinations_age_group_summary['date'].iloc[0])
    weekly_vaccinations_age_group_summary = weekly_vaccinations_age_group_summary.drop('date', axis=1)
    weekly_vaccinations_age_group_summary = weekly_vaccinations_age_group_summary.set_index('age_group')
    
    ax = weekly_vaccinations_age_group_summary.plot.bar(figsize=(15, 10), legend=True)
    ax.set_xlabel('Age Group', fontdict={'fontsize': 16})
    ax.set_ylabel('Percentage of people', fontdict={'fontsize': 16})
    ax.set_title("Percentage of people vaccinated by age group", fontdict={'fontsize': 20})
    plt.show()