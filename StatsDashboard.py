from sklearn.linear_model import LinearRegression
import scipy.stats as stats
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Dashboard import Dashboard


class StatsDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)

    def showCountriesDeathsOverCasesBoxPlot(self, ax):
        box = ax.boxplot(x=self.datasets['deaths_over_cases_%'], 
                         vert=False,
                         showmeans=True)
        ax.set_yticks([])
        ax.set_xlabel("Countries Deaths Over Cases %")
        
        x, y = box['medians'][0].get_xydata()[1]
        text = ' Î¼={:.2f}\n Ïƒ={:.2f}'.format(self.datasets['deaths_over_cases_%'].mean(), self.datasets['deaths_over_cases_%'].std())
        ax.annotate(text, xy=(x, y))
        
    def showCasesOverPopulationPercentByPoverty(self, ax):
        sns.scatterplot(x="poverty_%", 
                        y="cases_over_pop_%", 
                        data=self.datasets, 
                        hue="continent", 
                        ax=ax)
        ax.set_xlabel("% of Poverty")
        ax.set_ylabel("% of Cases Over Population")
        ax.axvline(x=6, linestyle='--')
        ax.axhline(y=2, linestyle='--')
        
    def showPeopleVaccinatedPercentByPoverty(self, ax):
        sns.scatterplot(x="poverty_%", 
                        y="people_1st_dose_%", 
                        data=self.datasets, 
                        hue="continent", 
                        ax=ax)
        ax.set_xlabel("% of Poverty")
        ax.set_ylabel("% of People Vaccinated (At Least 1st Dose)")
        ax.axvline(x=6, linestyle='--')
        ax.axhline(y=50, linestyle='--')
        
    def showLogCasesAndDeathsRegression(self, ax):
        self.datasets.plot.scatter(x="cumulative_deaths_log",
                                   y="cumulative_cases_log",
                                   ax=ax,
                                   label="(ln(deaths), ln(cases))")
        
        cumulative_deaths_log = np.array(self.datasets['cumulative_deaths_log']).reshape(-1, 1)
        cumulative_cases_log = np.array(self.datasets['cumulative_cases_log']).reshape(-1, 1)
        linear_regressor = LinearRegression()
        linear_regressor.fit(cumulative_deaths_log, cumulative_cases_log)
        cumulative_cases_pred = linear_regressor.predict(cumulative_deaths_log)
        ax.plot(cumulative_deaths_log, 
                cumulative_cases_pred, 
                color='red', 
                label="Linear Regression")
        ax.set_xlabel("ln(Cumulative Deaths)")
        ax.set_ylabel("ln(Cumulative Cases)")
        ax.legend()
        
    def showPeopleVaccinatedBasedOnCasesPercent(self, ax):
        sns.scatterplot(x="cases_over_pop_%", 
                        y="people_1st_dose_%", 
                        data=self.datasets, 
                        hue="continent", 
                        ax=ax)
        ax.set_xlabel("% of Cases Over Population")
        ax.set_ylabel("% of People Vaccinated (At Least 1st Dose)")
        ax.axvline(x=2, linestyle='--')
        ax.axhline(y=50, linestyle='--')
        
    def showDeathsOverPopulationPercentByPoverty(self, ax):
        sns.scatterplot(x="poverty_%", 
                        y="deaths_over_pop_%", 
                        data=self.datasets, 
                        hue="continent", 
                        ax=ax)
        ax.set_xlabel("% of Poverty")
        ax.set_ylabel("% of Deaths Over Population")
        ax.axvline(x=6, linestyle='--')
        ax.axhline(y=0.05, linestyle='--')