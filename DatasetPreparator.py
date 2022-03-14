import pandas as pd
import numpy as np


def mergeCasesAndDeathsDatasets(cases, deaths):
    # Merge the confirmed cases with deaths.
    cases_deaths = pd.merge(cases, deaths, on=['Province/State', 'Country/Region', 'Lat', 'Long', 'date'], how="inner")
    cases_deaths = cases_deaths.rename({'Province/State': 'state', 'Country/Region': 'entity', 'Lat': 'latitude', 'Long': "longitude"}, axis='columns')
    cases_deaths.loc[cases_deaths['state'] == "", 'state'] = cases_deaths['entity']

    #wrong_country_names = list(set(daily_cases_by_country['entity']) - set(population['entity']))
    wrong_country_names = ['West Bank and Gaza', 'Micronesia', 'Cabo Verde', 'Congo (Kinshasa)', 'Taiwan*', 'Korea, South', 'US', 'Timor-Leste', 'Burma', 'Congo (Brazzaville)']
    true_country_names = ['Palestine', 'Micronesia (country)', 'Cape Verde', 'Democratic Republic of Congo', 'Taiwan', 'South Korea', 'United States', 'Timor', 'Myanmar', 'Congo']

    for i, name in enumerate(wrong_country_names):
        cases_deaths.loc[cases_deaths['entity'] == name, 'entity'] = true_country_names[i]

    return cases_deaths

def prepareWorldDailyCasesAndDeathsDataset(cases_deaths):
    cases_by_date = cases_deaths.groupby(['date']) \
                                .agg(total_cases=pd.NamedAgg(column="confirmed_cases", aggfunc="sum"),
                                     total_deaths=pd.NamedAgg(column="deaths", aggfunc="sum")) \
                                .reset_index()

    cases_by_date['new_cases'] = cases_by_date['total_cases'].diff().fillna(0).astype(np.int64)
    cases_by_date['new_deaths'] = cases_by_date['total_deaths'].diff().fillna(0).astype(np.int64)

    return cases_by_date

def prepareRegionsDailyCasesAndDeathsDataset(cases_deaths):
    return cases_deaths.groupby(['entity', 'date']) \
                       .agg(total_cases=pd.NamedAgg(column="confirmed_cases", aggfunc="sum"),
                            total_deaths=pd.NamedAgg(column="deaths", aggfunc="sum")) \
                       .reset_index()

def prepareTotalCasesAndDeathsByRegion(daily_cases_by_region, population):
    cases_by_region = daily_cases_by_region.groupby(['entity']) \
                                           .agg({'total_cases': 'last', 'total_deaths': 'last'}) \
                                           .reset_index()

    cases_by_region = cases_by_region.rename({'total_cases': "Total cases", 'total_deaths': "Total deaths"}, axis='columns')
    cases_by_region = pd.merge(cases_by_region, population, on=['entity'], how="inner")
    #cases_by_region = cases_by_region.drop('iso_code', axis=1)

    cases_by_region['% of cases over population'] = round(cases_by_region['Total cases'] / cases_by_region['population'] * 100, 2)
    cases_by_region['% of deaths over population'] = round(cases_by_region['Total deaths'] / cases_by_region['population'] * 100, 2)
    cases_by_region['% of deaths over cases'] = round(cases_by_region['Total deaths'] / cases_by_region['Total cases'] * 100, 2)

    return cases_by_region
    
def addPeopleVaccinatedPercentageToDataset(dataset, vaccination):
    percentage_vaccinations = vaccination.groupby(['iso_code']) \
                                         .agg(people_vaccinated_percent=pd.NamedAgg(column="people_vaccinated_per_hundred", aggfunc="last")) \
                                         .reset_index()
    percentage_vaccinations['people_vaccinated_percent'] = percentage_vaccinations['people_vaccinated_percent'].astype(np.float64)
    return pd.merge(left=dataset,
                    right=percentage_vaccinations,
                    how="left",
                    on=['iso_code'])

def addContinentToPopulation(population, countries):
    return pd.merge(left=population,
                    right=countries,
                    how="left",
                    on=['iso_code'])
                    
def addPovertyToPopulation(population, poverty):
    return pd.merge(left=poverty, 
                    right=population, 
                    how="right", 
                    on=['iso_code'])
                    
def getVaccinationsByRegion(dataset, region):
    daily_vaccinations = dataset.loc[dataset['entity'] == region]
    daily_vaccinations = daily_vaccinations.drop(['entity', 'iso_code'], axis=1)
    daily_vaccinations.set_axis(labels=['date', 'total_vaccinations', 'people_1st_dose', 'people_2nd_dose', 'people_3rd_dose', 'daily_vaccinations', 
                                       '%_total_vaccinations', '%_people_1st_dose', '%_people_2nd_dose', '%_people_3rd_dose', 'daily_people_1st_dose', '%_daily_people_1st_dose'], 
                                    axis=1, 
                                    inplace=True)
    return daily_vaccinations