import pandas as pd
import numpy as np

def downloadCountriesDataset(url):
    countries = pd.read_csv(url, 
                            index_col=False, 
                            header=0, 
                            usecols=["alpha-3", "region"])
    countries = countries.rename({'alpha-3': 'iso_code', 'region': 'continent'}, axis='columns')
    
    return countries

def extractPovertyValueFromDataset(filename):
    poverty = pd.read_csv(filename, 
                          index_col=False, 
                          header=0, 
                          usecols=["SpatialDimValueCode", "IsLatestYear", "Value"])
    poverty = poverty.loc[poverty["IsLatestYear"] == True]
    poverty = poverty.drop(['IsLatestYear'], axis=1)
    poverty = poverty.rename({'SpatialDimValueCode': 'iso_code', 'Value': 'poverty_%'}, axis='columns')
    
    return poverty

def downloadPopulationDataset(url):
    population = pd.read_csv(url, usecols=['entity', 'iso_code', 'population'])
    population.loc[population['iso_code'] == "OWID_KOS", "iso_code"] = "KOS"
    population.loc[population['iso_code'] == "OWID_CIS", "iso_code"] = "CIS"
    population.loc[population['iso_code'] == "OWID_WRL", "iso_code"] = "WRL"

    # Remove all rows having their iso_code starting with "OWID_".
    return population[~population['iso_code'].str.startswith("OWID_", na=False)]

def downloadVaccinationsDataset(url):
    vaccination = pd.read_csv(url, dtype=str).fillna(0)
    vaccination = vaccination.rename({'location': 'entity'}, axis='columns')
    vaccination = vaccination.drop(['daily_vaccinations_raw', 'daily_vaccinations_per_million'], axis=1)

    vaccination['total_vaccinations'] = vaccination['total_vaccinations'].astype(np.int64)
    vaccination['people_vaccinated'] = vaccination['people_vaccinated'].astype(np.int64)
    vaccination['people_fully_vaccinated'] = vaccination['people_fully_vaccinated'].astype(np.int64)
    vaccination['total_boosters'] = vaccination['total_boosters'].astype(np.int64)
    vaccination['daily_vaccinations'] = vaccination['daily_vaccinations'].astype(np.int64)
    vaccination['daily_people_vaccinated'] = vaccination['daily_people_vaccinated'].astype(np.int64)

    return vaccination

def downloadVaccinationsByManufacturerDataset(url):
    vaccinations_by_manufacturer = pd.read_csv(url, dtype=str).fillna(0)
    vaccinations_by_manufacturer = vaccinations_by_manufacturer.rename({'location': 'entity'}, axis='columns')
    vaccinations_by_manufacturer['total_vaccinations'] = vaccinations_by_manufacturer['total_vaccinations'].astype(np.int64)
    
    return vaccinations_by_manufacturer

def downloadVaccinationsByAgeGroupDataset(url):
    vaccinations_by_age_group = pd.read_csv(url, dtype=str).fillna(0)
    vaccinations_by_age_group = vaccinations_by_age_group.rename({'location': 'entity'}, axis='columns')
    vaccinations_by_age_group['people_fully_vaccinated_per_hundred'] = vaccinations_by_age_group['people_fully_vaccinated_per_hundred'].astype(float)
    vaccinations_by_age_group['people_vaccinated_per_hundred'] = vaccinations_by_age_group['people_vaccinated_per_hundred'].astype(float)
    vaccinations_by_age_group['people_with_booster_per_hundred'] = vaccinations_by_age_group['people_with_booster_per_hundred'].astype(float)

    return vaccinations_by_age_group

def downloadCasesDataset(url):
    cases = pd.read_csv(url).fillna("")

    # Change the date columns to rows for each country.
    cases = cases.melt(['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='date', value_name='confirmed_cases')
    cases = cases.sort_values(by=["Country/Region", "Province/State"], ascending=True)
    cases['date'] = pd.to_datetime(cases['date'], format="%m/%d/%y")
    cases['date'] = cases['date'].dt.strftime('%Y-%m-%d')

    return cases

def downloadDeathsDataset(url):
    deaths = pd.read_csv(url).fillna("")

    deaths = deaths.melt(['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='date', value_name='deaths')
    deaths = deaths.sort_values(by=["Country/Region", "Province/State"], ascending=True)
    deaths['date'] = pd.to_datetime(deaths['date'], format="%m/%d/%y")
    deaths['date'] = deaths['date'].dt.strftime('%Y-%m-%d')

    return deaths

def downloadHospitalizationsDataset(url):
    hospitalizations = pd.read_csv(url)

    hospitalizations = hospitalizations.drop('iso_code', axis=1)
    hospitalizations['value'] = hospitalizations['value'].astype(np.int64)
    
    return hospitalizations
