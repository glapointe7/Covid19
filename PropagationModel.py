from mpmath import hyp2f1
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import math

# Return the number of people susceptible to be infected.
def S(t, p, beta, S0):
    return(p / (1 + (p / S0 - 1) * np.exp(p * beta * t)))

# Return the cumulative number of people infected.
def C(t, p, beta, C0):
    return(p / (1 - (1 - p / C0) * np.exp(-p * beta * t)))

# Cumulative number of people that recovered from the infection.
def R(t, p, beta, gamma, C0, R0):
    delta = 1 - (p / C0)
    F1 = hyp2f1(1, 1 + (gamma/(p*beta)), 2 + (gamma/(p*beta)), np.exp(p * beta * t)/delta)

    return((-gamma * p * np.exp(p * beta * t) * F1) / (delta * (p * beta + gamma)) + (R0 * np.exp(-gamma * t)))

# Cumulative number of dead people from the infection.
def D(t, p, beta, alpha, C0, D0):
    delta = 1 - (p / C0)
    F1 = hyp2f1(1, 1 + (alpha/(p*beta)), 2 + (alpha/(p*beta)), np.exp(p * beta * t)/delta)

    return((-alpha * p * np.exp(p * beta * t) * F1) / (delta * (p * beta + alpha)) + (D0 * np.exp(-alpha * t)))

def createPropagationSimulation(initial_values, parameters):
    model = pd.DataFrame({'date': [initial_values['date']],
                          'cumulative_infected': [initial_values['C0']],
                          'recovered': [initial_values['R0']],
                          'deaths': [initial_values['D0']]})

    for t in range(1, parameters['days']):
        model = model.append({'date': pd.to_datetime(model['date'][t-1]) + pd.Timedelta(1, unit='D'),
                              'cumulative_infected': C(t, parameters['population'], parameters['beta'], initial_values['C0']),
                              'recovered': R(t, parameters['population'], parameters['beta'], parameters['gamma'], initial_values['C0'], initial_values['R0']),
                              'deaths': D(t, parameters['population'], parameters['beta'], parameters['alpha'], initial_values['C0'], initial_values['D0'])}, ignore_index=True)

    model['date'] = pd.to_datetime(model['date'], format='%Y-%m-%d')
    model['date'] = model['date'].dt.strftime('%Y-%m-%d')
    model['cumulative_infected'] = model['cumulative_infected'].astype(np.int64)
    model['recovered'] = model['recovered'].astype(np.int64)
    model['deaths'] = model['deaths'].astype(np.int64)

    model['susceptibles'] = parameters['population'] - model['cumulative_infected']
    model['active_infected'] = model['cumulative_infected'] - model['recovered'] - model['deaths']
    model = model.set_index('date')

    return model

def plotFeatureModel(model, feature, ax):
    model.plot(ax=ax, rot=90)
    ax.set_title("Time series simulation of the " + feature + " people", fontdict={'fontsize':24})
    ax.set_xlabel('Date', fontdict={'fontsize':20})
    ax.set_ylabel(feature, fontdict={'fontsize':20})
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

def plotModelSimulation(model):
    fig, axes = plt.subplots(2, 2, figsize=(20, 10))
    plotFeatureModel(model['active_infected'], "Active Infected", axes[0, 0])
    plotFeatureModel(model['cumulative_infected'], "Cumulative Infected", axes[0, 1])
    plotFeatureModel(model['recovered'], "Recovered", axes[1, 0])
    plotFeatureModel(model['deaths'], "Dead", axes[1, 1])
    fig.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    plt.show()

def findAberrantAccelerations(accelerations, n, tau):
    number_of_samples = math.ceil(len(accelerations) / n)
    samples = np.array_split(accelerations, number_of_samples)

    aberrants = []
    for sample in samples:
        sigma = np.std(sample)
        mu = np.mean(sample)
        z_scores = [(acceleration - mu) / sigma for acceleration in sample]
        aberrants.extend([True if np.abs(z_score) >= tau else 0 for z_score in z_scores])

    return aberrants
    
def plotAberrantAccelerations(daily_cases):
    aberrants = daily_cases.loc[daily_cases['is_aberrant'] == True, ['cases_acceleration']].reset_index()
    
    aberrants['date'] = pd.to_datetime(aberrants['date'], format='%Y-%m-%d')
    daily_cases = daily_cases.reset_index()
    daily_cases['date'] = pd.to_datetime(daily_cases['date'], format="%Y-%m-%d")
    
    ax = daily_cases.plot.line(x='date',
                               y='cases_acceleration',
                               label="Cases Acceleration", 
                               figsize=(20, 10))
    aberrants.plot.scatter(x='date',
                           y='cases_acceleration',
                           color='r', 
                           label='Aberrant accelerations Detection', 
                           ax=ax)
    ax.set_title("Time series of the propagation accelerations", fontdict={'fontsize':24})
    ax.set_xlabel('Date', fontdict={'fontsize':20})
    ax.set_ylabel('Acceleration', fontdict={'fontsize':20})
    ax.legend(loc="best", fontsize=14)
    
    plt.show()