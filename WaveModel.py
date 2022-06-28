from mpmath import hyp2f1
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import math
from Model import Model


class WaveModel(Model):
    #def __init__(self, parameters):
    #    super().__init__(parameters)
    
    # Return the cumulative number of people infected.
    def C(self, t):
        return(self.parameters['population'] / (1 - (1 - self.parameters['population'] / self.parameters['C0']) * np.exp(-self.parameters['population'] * self.parameters['beta'] * t)))
    
    # Cumulative number of dead people from the infection.
    def D(self, t):
        delta = 1 - (self.parameters['population'] / self.parameters['C0'])
        pop_times_beta = self.parameters['population'] * self.parameters['beta']
        exp_pop_times_beta = np.exp(pop_times_beta * t)
        alpha_pop_times_beta = self.parameters['alpha'] / pop_times_beta
        
        f1 = hyp2f1(1, 1 + alpha_pop_times_beta, 2 + alpha_pop_times_beta, exp_pop_times_beta / delta)
    
        return((-self.parameters['alpha'] * self.parameters['population'] * exp_pop_times_beta * f1) / (delta * (pop_times_beta + self.parameters['alpha'])) + (self.parameters['D0'] * np.exp(-self.parameters['alpha'] * t)))
    
    def create(self):
        model = pd.DataFrame({'date': [self.parameters['date']],
                              'cumulative_cases': [self.parameters['C0']],
                              'cumulative_deaths': [self.parameters['D0']]})
    
        for t in range(1, self.parameters['days']):
            model = model.append({'date': pd.to_datetime(model['date'][t-1]) + pd.Timedelta(1, unit='D'),
                                  'cumulative_cases': self.C(t),
                                  'cumulative_deaths': self.D(t)}, ignore_index=True)
    
        model['date'] = pd.to_datetime(model['date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
        model['cumulative_cases'] = model['cumulative_cases'].astype(np.int64)
        model['cumulative_deaths'] = model['cumulative_deaths'].astype(np.int64)
        model['susceptibles'] = self.parameters['population'] - model['cumulative_cases']
    
        return model.set_index('date')
    
    def showSimulationTimeSeries(self, model, feature, ax):
        model.plot(ax=ax, rot=90)
        ax.set_xlabel('Date', fontdict={'fontsize':20})
        ax.set_ylabel(feature, fontdict={'fontsize':20})
        ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    def buildDashboard(self, model):
        fig, axes = plt.subplots(2, 2, figsize=(20, 10))
        self.showSimulationTimeSeries(model['cumulative_cases'], "Cumulative Cases", axes[0, 0])
        self.showSimulationTimeSeries(model['susceptibles'], "Susceptibles", axes[0, 1])
        self.showSimulationTimeSeries(model['cumulative_deaths'], "Cumulative Deaths", axes[1, 0])
        axes[1, 1].axis('off')
        fig.tight_layout()
        plt.subplots_adjust(hspace=0.5)
        plt.show()