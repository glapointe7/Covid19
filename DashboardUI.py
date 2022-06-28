from IPython.display import display, clear_output
from DashboardCreator import DashboardCreator

# Import ipywidgets for having a UI to select an item from a dropdown list.
import Utils
Utils.installPackageIfNotInstalled("ipywidgets")
import ipywidgets as widgets


class DashboardUI:
    def __init__(self, datasets):
        self.datasets = datasets
        self.entity_drop_down = None
        self.dashboard_drop_down = None
        self.button = None
    
    
    def onButtonClick(self, button):
        clear_output()
        display(self.dashboard_drop_down, self.entity_drop_down, self.button)
        
        if self.entity_drop_down.value != '-' and self.dashboard_drop_down.value != '(Select a dashboard)':
            # Entities with a 3-character iso code are not a continent or World.
            if self.entity_drop_down.value not in ['AF', 'NA', 'SA', 'AS', 'EU', 'OC', 'WR']:
                datasets = {key: value.filterByEntity(self.entity_drop_down.value) for key, value in self.datasets.items()}
            else:
                datasets = {key: value.dataset for key, value in self.datasets.items()}
                datasets['summary'] = self.datasets['summary'].prepareContinentOrWorld(self.entity_drop_down.value, self.datasets)

            dashboard_creator = DashboardCreator()
            dashboard_creator.setBuilder(self.dashboard_drop_down.value, datasets)
            if dashboard_creator.builder is not None:
                dashboard_creator.builder.build()
            else:
                entity = self.datasets['countries'].getEntityNameFromISOCode(self.entity_drop_down.value)
                display("There are no data found for the entity " + entity)
    
    
    def onDashboardChange(self, dashboard_selected):
        options = []
        if dashboard_selected.new == 'Cases and deaths':
            options = self.datasets['cases_and_deaths'].getEntityList()
        elif dashboard_selected.new == 'Vaccinations':
            options = self.datasets['vaccinations'].getEntityList()
        elif dashboard_selected.new == 'Hospitalizations':
            options = self.datasets['hospitalizations'].getEntityList()
        elif dashboard_selected.new == 'Tests':
            options = self.datasets['tests'].getEntityList()
        elif dashboard_selected.new == 'Stringency':
            options = self.datasets['stringency'].getEntityList()
        elif dashboard_selected.new == 'Summary':
            options = [('World', 'WR')] + self.datasets['countries'].getContinentList() + self.datasets['countries'].getEntityList()
 
        self.entity_drop_down.options = [("(Select an entity)", "-")] + options
    
    
    def show(self):
        dashboard_options = ['(Select a dashboard)', 'Summary', 'Cases and deaths', 'Vaccinations', 'Hospitalizations', 'Tests', 'Stringency']
        self.dashboard_drop_down = widgets.Dropdown(options=dashboard_options,
                                                    value=dashboard_options[0],
                                                    description="Dashboard")
        
        entity_options = [("(Select an entity)", "-")]
        self.entity_drop_down = widgets.Dropdown(options=entity_options,
                                                 value=entity_options[0][1],
                                                 description="Entity")
        
        self.button = widgets.Button(
            description='Display Dashboard',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Display a dashboard based on the country selected.'
        )                
        
        display(self.dashboard_drop_down, self.entity_drop_down, self.button)
        self.dashboard_drop_down.observe(self.onDashboardChange, names='value')
        self.button.on_click(self.onButtonClick)