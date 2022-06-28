from IPython.display import display


class CountriesDatasetViewer:
    def __init__(self):
        self.countries = DatasetController()
        
    def show(self):
        display(self.countries)
