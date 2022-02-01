import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from IPython.display import display
from tabulate import tabulate

import Utils
import CasesDeathsPreparator


def plotCasesByDate(cases):
    ax = cases['total_cases'].plot(label="Cases")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of cases', fontsize=16)
    plt.title("Number of cases in function of the date", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotDeathsByDate(deaths):
    ax = deaths['total_deaths'].plot(label="Deaths")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of deaths', fontsize=16)
    plt.title("Number of deaths in function of the date", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotNewCasesByDate(new_cases):
    ax = new_cases['new_cases'].plot(label="New Cases")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of cases', fontsize=16)
    plt.title("Number of new daily cases", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotNewDeathsByDate(new_deaths):
    ax = new_deaths['new_deaths'].plot(label="New Deaths")

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of deaths', fontsize=16)
    plt.title("Number of new daily deaths", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def displayCumulativeSummary(dataset, region):    
    print(Utils.Color.BOLD + region + " Confirmed Cases and Deaths Summary\n" + Utils.Color.END)
    print(tabulate(tabular_data=dataset, 
                    showindex=False, 
                    disable_numparse=True, 
                    headers=['Total Cases', 'Total Deaths', 'Population', '% of Cases Over Pop.', '% of Deaths Over Pop.', '% of Deaths over Cases', 'New Cases', 'New Deaths']) + "\n")
    

def displayWorldSummary(dataset, population):
    world_daily_cases = CasesDeathsPreparator.prepareWorldDailyCasesAndDeathsDataset(dataset)
    world_population = population.loc[population['entity'] == "World", 'population'].iloc[0]

    world_cases_dict = {'total_cases': [world_daily_cases['total_cases'].iloc[-1]],
                        'total_deaths': [world_daily_cases['total_deaths'].iloc[-1]],
                        'population': [world_population],
                        'total_cases_population_%': [round(world_daily_cases['total_cases'].iloc[-1] / world_population * 100, 4)],
                        'total_deaths_population_%': [round(world_daily_cases['total_deaths'].iloc[-1] / world_population * 100, 4)],
                        'total_deaths_cases_%': [round(world_daily_cases['total_deaths'].iloc[-1] / world_daily_cases['total_cases'].iloc[-1] * 100, 4)],
                        'new_cases': [world_daily_cases['new_cases'].iloc[-1]],
                        'new deaths': [world_daily_cases['new_deaths'].iloc[-1]]}
    world_cases = pd.DataFrame(data=world_cases_dict)
    displayCumulativeSummary(world_cases, "World")

    world_daily_cases = world_daily_cases.set_index('date')
    plt.figure(figsize=(25, 15))
    ax1 = plt.subplot(2,2,1)
    plotCasesByDate(world_daily_cases)
    ax2 = plt.subplot(2,2,2)
    plotDeathsByDate(world_daily_cases)
    ax3 = plt.subplot(2,2,3)
    plotNewCasesByDate(world_daily_cases)
    ax4 = plt.subplot(2,2,4)
    plotNewDeathsByDate(world_daily_cases)
    plt.subplots_adjust(hspace=0.5)
    plt.show()

def displayRegionSummary(dataset, population, region):
    daily_cases = CasesDeathsPreparator.prepareRegionsDailyCasesAndDeathsDataset(dataset)
    daily_cases = daily_cases.loc[daily_cases['entity'] == region]
    daily_cases['new_cases'] = daily_cases['total_cases'].diff().fillna(0).astype(np.int64)
    daily_cases['new_deaths'] = daily_cases['total_deaths'].diff().fillna(0).astype(np.int64)

    region_cases = CasesDeathsPreparator.prepareTotalCasesAndDeathsByRegion(daily_cases, population)
    region_cases = region_cases.drop('entity', axis=1)
    region_cases['new_cases'] = daily_cases['new_cases'].iloc[-1]
    region_cases['new_deaths'] = daily_cases['new_deaths'].iloc[-1]
    displayCumulativeSummary(region_cases, region)

    daily_cases = daily_cases.set_index('date')
    plt.figure(figsize=(25, 15))
    ax1 = plt.subplot(2,2,1)
    plotCasesByDate(daily_cases)
    ax2 = plt.subplot(2,2,2)
    plotDeathsByDate(daily_cases)
    ax3 = plt.subplot(2,2,3)
    plotNewCasesByDate(daily_cases)
    ax4 = plt.subplot(2,2,4)
    plotNewDeathsByDate(daily_cases)
    plt.subplots_adjust(hspace=0.5)
    plt.show()
