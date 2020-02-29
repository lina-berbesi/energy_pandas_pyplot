
import pandas as pd

opsd_daily = pd.read_csv('XM\opsd_germany_daily.csv')

opsd_daily.shape

opsd_daily.head(3)

opsd_daily.tail(3)

opsd_daily.dtypes

opsd_daily['Date'] = pd.to_datetime(opsd_daily['Date'], format='%Y-%m-%d')

opsd_daily = opsd_daily.set_index('Date')

opsd_daily.index

opsd_daily['Year'] = opsd_daily.index.year
opsd_daily['Month'] = opsd_daily.index.month
opsd_daily['Weekday Name'] = opsd_daily.index.weekday_name

# Display a random sampling of 5 rows
opsd_daily.sample(5, random_state=0)

#accesing data with datetime index and loc accessor

opsd_daily.loc['2017-08-10']

opsd_daily.loc['2014-01-20':'2014-01-22']

import matplotlib.pyplot as plt
import seaborn as sns

#sns.set(rc={'figure.figsize':(11, 4)})
fig12, ax12 =plt.subplots()
opsd_daily['Consumption'].plot(linewidth=0.5, ax=ax12)
plt.title('Germany Daily Consumption (GWh)')

cols_plot = ['Consumption', 'Solar', 'Wind']
axes = opsd_daily[cols_plot].plot(marker='.', alpha=0.5, linestyle='None', figsize=(11, 9), subplots=True)
for ax in axes:
    ax.set_ylabel('Daily Totals (GWh)')



