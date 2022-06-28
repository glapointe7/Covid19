import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from Dashboard import Dashboard
import Utils


class VaccinationsDashboard(Dashboard):
    def __init__(self, datasets):
        super().__init__(datasets)

    def showCumulativeVaccinationsTimeSeries(self, ax):
        self.datasets['general']['cumulative_vaccines'].plot(label="Total Vaccinations", ax=ax, rot=90)
        
        ax.set_xlabel('Date', fontdict={'fontsize': 14})
        ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 14})
        ax.set_title("Time series of the cumulative number of vaccins administrated", fontdict={'fontsize': 16})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    def showNewVaccinationsTimeSeries(self, ax):
        self.datasets['general']['new_vaccines'].plot(label="Daily Total Vaccinations", ax=ax, rot=90)
        
        ax.set_xlabel('Date', fontdict={'fontsize': 14})
        ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 14})
        ax.set_title("Time series of the number of new vaccins administrated", fontdict={'fontsize': 16})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    def showCumulativeVaccinationsByDoseTimeSeries(self, ax):
        self.datasets['general']['people_1st_dose'].plot(label="People with 1st Dose", ax=ax, rot=90, legend=True)
        self.datasets['general']['people_2nd_dose'].plot(label="People with 2nd Dose", ax=ax, rot=90, legend=True)
        self.datasets['general']['people_3rd_dose'].plot(label="People with 3rd Dose", ax=ax, rot=90, legend=True)

        ax.set_xlabel('Date', fontdict={'fontsize': 14})
        ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 14})
        ax.set_title("Time series of the cumulative number of \n1st, 2nd and 3rd doses administrated", fontdict={'fontsize': 16})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    def showNewFirstDoseVaccinationsTimeSeries(self, ax):
        self.datasets['general']['new_people_1st_dose'].plot(label="People with 1st Dose", ax=ax, rot=90)
        
        ax.set_xlabel('Date', fontdict={'fontsize': 14})
        ax.set_ylabel('Number of vaccins', fontdict={'fontsize': 14})
        ax.set_title("Time series of the number of new first doses administrated", fontdict={'fontsize': 16})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
        
    def showCumulativeVaccinationsByDoseBarChart(self, ax):
        vaccins = pd.DataFrame({'doses': ["Total vaccins", "Total 1st dose", "Total 2nd dose", "Total 3rd dose"], 
                                'number_of_vaccins': [self.datasets['general'].iloc[[-1]]['cumulative_vaccines'].iloc[0], 
                                                      self.datasets['general'].iloc[[-1]]['people_1st_dose'].iloc[0],
                                                      self.datasets['general'].iloc[[-1]]['people_2nd_dose'].iloc[0], 
                                                      self.datasets['general'].iloc[[-1]]['people_3rd_dose'].iloc[0]]})

        vaccins.set_index('doses').plot.barh(ax=ax, legend=False)
        ax.set_xlabel('People vaccinated', fontdict={'fontsize': 14})
        ax.set_ylabel('')
        ax.set_title("Number of people vaccinated by \nnumber of doses", fontdict={'fontsize': 16})
        ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.tick_params(axis='x', rotation=90)
        
        percentages = [self.datasets['general'].iloc[[-1]]['cumulative_vaccines_%'].iloc[0], 
                       self.datasets['general'].iloc[[-1]]['people_1st_dose_%'].iloc[0], 
                       self.datasets['general'].iloc[[-1]]['people_2nd_dose_%'].iloc[0], 
                       self.datasets['general'].iloc[[-1]]['people_3rd_dose_%'].iloc[0]]
        for i, bar in enumerate(ax.patches):
            ax.annotate(str(int(bar.get_width())) + "   [" + str(percentages[i]) + " %]",
                        (bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2),
                        color='orange',
                        weight='bold',
                        fontsize=10)
    

    def showCumulativeVaccinationsPieChart(self, ax):
        people_1st_dose = float(self.datasets['general'].iloc[[-1]]['people_1st_dose_%'].iloc[0])
        people_2nd_dose = float(self.datasets['general'].iloc[[-1]]['people_2nd_dose_%'].iloc[0])
        people_3rd_dose = float(self.datasets['general'].iloc[[-1]]['people_3rd_dose_%'].iloc[0])
        
        vaccination_percentage = {
            "Not Vaccinated": 100.0 - people_1st_dose,
            "1st Dose Only": people_1st_dose - people_2nd_dose,
            "1st and 2nd Doses": people_2nd_dose - people_3rd_dose,
            "All 3 Doses": people_3rd_dose
        }
       
        ax.pie(x=list(vaccination_percentage.values()), 
               labels=vaccination_percentage.keys(), 
               autopct='%1.1f%%', 
               textprops={'fontsize': 14},
               shadow=True)
        ax.set_title("Percentage of people having their 1st dose only, \n1st and 2nd doses only, and all doses", fontdict={'fontsize': 16})
        
        
    def showWeeklyVaccinationsByManufacturerTimeSeries(self, ax):
        self.datasets['by_manufacturer'].groupby('manufacturer')['cumulative_vaccines'] \
                                        .plot(legend=True, ax=ax, rot=90)
    
        ax.set_xlabel('Date', fontdict={'fontsize': 14})
        ax.set_ylabel('Number of vaccinations', fontdict={'fontsize': 14})
        ax.set_title("Number of weekly people vaccinated by vaccine manufacturer", fontdict={'fontsize': 16})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        
    def showCumulativeVaccinationsByManufacturerBarChart(self, ax):
        weekly_vaccinations_summary = self.datasets['by_manufacturer'].groupby(['manufacturer']).last()
        weekly_vaccinations_summary.plot.barh(legend=False, ax=ax, rot=90)

        ax.set_xlabel('People vaccinated', fontdict={'fontsize': 14})
        ax.set_ylabel('')
        ax.set_title("Total number of people vaccinated by manufacturer", fontdict={'fontsize': 16})
        ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.tick_params(axis='x', rotation=90)
        ax.tick_params(axis='y', rotation=45)
        
        cumulative_vaccines = np.sum(weekly_vaccinations_summary['cumulative_vaccines'])
        percentages = round(weekly_vaccinations_summary['cumulative_vaccines'] / cumulative_vaccines * 100, 2)
        for i, bar in enumerate(ax.patches):
            ax.annotate(str(int(bar.get_width())) + "   [" + str(percentages[i]) + " %]",
                        (bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2),
                        color='orange',
                        weight='bold',
                        fontsize=10)
            
    def showCumulativeVaccinationsByAgeBarChart(self, ax):
        weekly_vaccinations_age_group_summary = self.datasets['by_age'].groupby(['age_group']).last()
        weekly_vaccinations_age_group_summary.plot.bar(legend=True, ax=ax)
        
        ax.set_xlabel('Age Group', fontdict={'fontsize': 14})
        ax.set_ylabel('Percentage of people', fontdict={'fontsize': 14})
        ax.set_title("Percentage of people vaccinated by age group", fontdict={'fontsize': 16})
        plt.show()