# Summary
This analysis contains:

- A dashboard of cases, deaths, vaccinations and hospitalizations based on a region selected;
- A table of countries displaying the cumulative number of cases, deaths, and percentages;
- A mathematical model of aberrant propagation accelerations detection;
- The steps of defining a basic propagation velocity mathematical model;
- A simulation of the propagation model.

# Dashboard
Based on a region selected in a dropdown list, the dashboard presents:

- The cumulative number of cases and death;
- The new daily cases and deaths;
- The percentages of people not vaccinated, with only the first dose, with first and second doses, and with all 3 doses;
- The number of people vaccinated with at least one dose, at least 2 doses and all 3 doses;
- The cumulative total number of vaccins administrated;
- The new daily number of vaccins administrated;
- The cumulative number of people vaccinated with at least one dose, at least 2 doses and all 3 doses;
- The new daily number of first dose administrated;
- The new daily number of people hospitalized and intensive care (ICU);
- The number of people hospitalized per million people;
- The number of vaccins administrated per manufacturer (e.g. Moderna, Pfizer);
- The number of vaccins (first, second and third doses) administrated per age group (e.g. 0-17 years old, 18-25 years old).

If some of the presentations are not shown in the dashboard, it means that the dataset does not have any information on the region selected.

# Model Simulation
We built a basic SIRD epidemic model to simulate a basic approximation of a propagation wave. 
A complete demonstration shows how to obtain the final differential equations system and their solutions.
Then, we display a table and plots of our simulation. 
By basic model, we mean that it does not include the vaccinations, safety measures, births and deaths (not related to the virus) and any other variables.

# Files
The way we created the Python files is to separate the display from the data preparation among the cases and deaths, vaccinations and hospitalizations datasets:
- The Printer files are used for printing data and for plots. 
- The Preparator files are used for preparing the data in a form that the Printer functions are able to process easily.
- The PropagationModel file is used for the model simulation and for the aberrant accelerations detection.
- The DatasetDownloader file is used for reading CSV stored on Github by OWID into a data frame that we clean afterwards.
