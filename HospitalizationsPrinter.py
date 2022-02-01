import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plotDailyHospitalizations(daily_hospitalizations):
    columns = daily_hospitalizations.columns.to_list()
    columns = filter(lambda column: not column.endswith('million'), columns)
    for column in columns:
        daily_hospitalizations[column].plot()

    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Number of hospitalizations', fontsize=16)
    plt.title("Number of daily people hospitalized", fontsize=20)
    plt.ticklabel_format(style='plain', axis='y')
    plt.tick_params(axis='x', rotation=90)
    plt.legend()

def plotHospitalizationsPerMillionBarChart(dataset):
    ax = dataset.plot(kind='barh')
    plt.xlabel('Hospitalizations per million', fontsize=16)
    plt.title("Number of people hospitalized per million", fontsize=20)
    
    for i, value in enumerate(dataset):
        ax.text(value / 3, i, str(value), color='black', fontsize=14)