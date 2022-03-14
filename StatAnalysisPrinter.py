from sklearn.linear_model import LinearRegression
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
import DatasetPreparator

def displayCorrelationMatrix(region_cases):
    corr = region_cases.drop(['entity', 'continent'], axis=1).corr()
    
    display(corr.style.background_gradient(cmap='coolwarm').format('{:.2f}'))


def scatterPlot(region_cases):
    region_cases['Total cases'] = np.array(region_cases['Total cases'], dtype = float)
    region_cases['Total deaths'] = np.array(region_cases['Total deaths'], dtype = float)
    region_cases['Total cases log'] = np.log(region_cases['Total cases'], out=np.zeros_like(region_cases['Total cases']), where=(region_cases['Total cases']!=0))
    region_cases['Total deaths log'] = np.log(region_cases['Total deaths'], out=np.zeros_like(region_cases['Total deaths']), where=(region_cases['Total deaths']!=0))

    fig, axes = plt.subplots(3, 2, figsize=(20, 20))
    sns.scatterplot(x="poverty_%", 
                    y="% of cases over population", 
                    data=region_cases, 
                    hue="continent", 
                    ax=axes[0, 0])
    axes[0, 0].set_title("% of cases over population based on the % of poverty grouped by continent")
    axes[0, 0].axvline(x=7, linestyle='--')
    axes[0, 0].axhline(y=1, linestyle='--')

    sns.scatterplot(x="poverty_%", 
                    y="people_vaccinated_percent", 
                    data=region_cases, 
                    hue="continent", 
                    ax=axes[0, 1])
    axes[0, 1].set_title("% of people vaccinated based on the % of poverty grouped by continent")
    axes[0, 1].axvline(x=7, linestyle='--')
    axes[0, 1].axhline(y=50, linestyle='--')

    region_cases.plot.scatter(x="Total deaths log",
                              y="Total cases log",
                              ax=axes[1, 0],
                              label="Points (ln(deaths), ln(cases))")

    total_deaths_log = np.array(region_cases['Total deaths log']).reshape(-1, 1)
    total_cases_log = np.array(region_cases['Total cases log']).reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(total_deaths_log, total_cases_log)
    total_cases_pred = linear_regressor.predict(total_deaths_log)

    axes[1, 0].plot(total_deaths_log, 
                    total_cases_pred, 
                    color='red', 
                    label="Linear Regression")
    axes[1, 0].set_title("Scatter plot of natural log of total cases based on natural log of total deaths with linear regression")
    axes[1, 0].legend()

    sns.scatterplot(x="% of cases over population", 
                    y="people_vaccinated_percent", 
                    data=region_cases, 
                    hue="continent", 
                    ax=axes[1, 1])
    axes[1, 1].set_title("% of people vaccinated based on the percentage of cases grouped by continent")
    
    sns.scatterplot(x="poverty_%", 
                    y="% of deaths over population", 
                    data=region_cases, 
                    hue="continent", 
                    ax=axes[2, 0])
    axes[2, 0].set_title("% of deaths over population based on the % of poverty grouped by continent")
    axes[2, 0].axvline(x=7, linestyle='--')
    axes[2, 0].axhline(y=0.05, linestyle='--')
    
    axes[2, 1].axis('off')

    plt.show()