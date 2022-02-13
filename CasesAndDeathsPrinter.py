import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import scipy.stats as stats
from tabulate import tabulate

import Utils
import CasesDeathsPreparator

def plotCasesDeathsTimeSeries(dataset, feature, ax):
    dataset.plot(label=feature, ax=ax, rot=90)
    ax.set_xlabel('Date', fontdict={'fontsize': 16})
    ax.set_ylabel(feature, fontdict={'fontsize': 16})
    ax.set_title("Time series of the " + feature, fontdict={'fontsize': 20})
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
    
    fig, axes = plt.subplots(2, 2, figsize=(25, 15))
    plotCasesDeathsTimeSeries(world_daily_cases['total_cases'], "Cumulative Cases", axes[0, 0])
    plotCasesDeathsTimeSeries(world_daily_cases['total_deaths'], "Deaths", axes[0, 1])
    plotCasesDeathsTimeSeries(world_daily_cases['new_cases'], "New Cases", axes[1, 0])
    plotCasesDeathsTimeSeries(world_daily_cases['new_deaths'], "New Deaths", axes[1, 1])
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
    fig, axes = plt.subplots(2, 2, figsize=(25, 15))
    plotCasesDeathsTimeSeries(daily_cases['total_cases'], "Cumulative Cases", axes[0, 0])
    plotCasesDeathsTimeSeries(daily_cases['total_deaths'], "Deaths", axes[0, 1])
    plotCasesDeathsTimeSeries(daily_cases['new_cases'], "New Cases", axes[1, 0])
    plotCasesDeathsTimeSeries(daily_cases['new_deaths'], "New Deaths", axes[1, 1])
    plt.subplots_adjust(hspace=0.5)
    plt.show()

def plotAccelerationNormalDistribution(dataset, feature, ax):
    mu, sigma = stats.norm.fit(dataset)
    x = np.linspace(mu - 5*sigma, mu + 5*sigma, len(dataset))
    y = stats.norm.pdf(x, mu, sigma)
    plot_title = feature + r" Acceleration normal distribution ($\mu = " + str(round(mu, 4)) + "; \sigma = " + str(round(sigma, 4)) + ")$"
    
    ax.plot(x, y)
    ax.set_xlabel(feature + ' Acceleration', fontdict={'fontsize': 14})
    ax.set_ylabel('Probability Density', fontdict={'fontsize': 14})
    ax.set_title(plot_title, fontdict={'fontsize': 17})

def plotAccelerationData(dataset, feature, ax):
    dataset.plot(ax=ax, legend=False, rot=90)
    ax.set_xlabel('Date', fontdict={'fontsize': 14})
    ax.set_ylabel(feature + ' Acceleration', fontdict={'fontsize': 14})
    ax.set_title(feature + " daily acceleration", fontdict={'fontsize': 17})