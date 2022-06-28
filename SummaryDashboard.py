import Utils
Utils.installPackageIfNotInstalled("plotly")
import plotly.graph_objects as go
from Dashboard import Dashboard


class SummaryDashboard(Dashboard):
    def __init__(self, dataset):
        super().__init__(dataset)
        
    def showLatestCases(self, fig):
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = self.datasets['cumulative_cases'].iloc[0],
            number = {'valueformat':',d'},
            title = {"text": "Cases"},
            delta = {'reference': self.datasets['cumulative_cases'].iloc[0] - self.datasets['new_cases'].iloc[0], 'valueformat':',d'},
            domain = {'row': 0, 'column': 0}))
            
    def showLatestDeaths(self, fig):
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = self.datasets['cumulative_deaths'].iloc[0],
            number = {'valueformat':',d'},
            title = {"text": "Deaths"},
            delta = {'reference': self.datasets['cumulative_deaths'].iloc[0] - self.datasets['new_deaths'].iloc[0], 'valueformat':',d'},
            domain = {'row': 0, 'column': 1}))
            
    def showCasesOverPopulation(self, fig):
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            number = {'suffix': '%', 'valueformat': '.1f'},
            value = self.datasets['cases_over_pop_%'].iloc[0],
            title = {"text": "Cases over Population %"},
            domain = {'row': 1, 'column': 0},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': 'green'},
                    {'range': [30, 50], 'color': 'yellow'},
                    {'range': [50,100], 'color': 'red'}],
                }))
                
    def showPeopleWithAtLeast2ndDose(self, fig):
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            number = {'suffix': '%', 'valueformat': '.1f'},
            value = self.datasets['people_2nd_dose_%'].iloc[0],
            title = {"text": "People with at least a 2nd dose %"},
            domain = {'row': 1, 'column': 1},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': 'red'},
                    {'range': [50, 80], 'color': 'yellow'},
                    {'range': [80,100], 'color': 'green'}],
                }))