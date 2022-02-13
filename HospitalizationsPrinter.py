import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plotDailyHospitalizations(dataset, ax):
    columns = dataset.columns.to_list()
    columns = filter(lambda column: not column.endswith('million'), columns)
    for column in columns:
        dataset[column].plot(legend=True, ax=ax, rot=90)

    ax.set_xlabel('Date', fontdict={'fontsize': 16})
    ax.set_ylabel('Hospitalizations', fontdict={'fontsize': 16})
    ax.set_title("Time series of the number of new hospitalizations", fontdict={'fontsize': 20})

def plotHospitalizationsPerMillionBarChart(dataset, ax):
    dataset.plot.barh()
    ax.set_xlabel('Hospitalizations per million', fontdict={'fontsize': 16})
    ax.set_title("Number of hospitalizations per million by type of hospitalization", fontdict={'fontsize': 20})
    
    for i, value in enumerate(dataset):
        ax.text(x=value / 3, 
                y=i, 
                s=str(value), 
                color='black', 
                fontsize=14)