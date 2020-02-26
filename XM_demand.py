import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns

df = pd.read_excel('XM\Demanda_por_OR_2010.xlsx', skiprows=2)

df.drop('Version', axis=1, inplace=True)

df.rename(columns={'Fecha': 'date', 'Código Distribuidor': 'distributor_code'}, inplace=True)

df_demand = pd.melt(df, id_vars=['date','distributor_code'], value_vars=['0', '1', '2', '3', '4', '5', '6', '7', '8',
       '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
       '21', '22', '23'],var_name='hours', value_name='demand').sort_values(['date','distributor_code']).reset_index(drop=True)

df_demand = df_demand[['date', 'hours', 'demand', 'distributor_code']]

df_demand['hours'] = pd.to_datetime(pd.to_numeric(df_demand['hours']), format='%H').dt.strftime("%H:%M:%S")

df_demand['date_time'] = pd.to_datetime(df_demand['date'] + ' ' + df_demand['hours'])

df_demand['demand_thous'] = df_demand['demand']/1e3

df_demand['quarter'] = df_demand['date_time'].dt.quarter

df_demand = df_demand[['date_time', 'demand', 'demand_thous', 'distributor_code', 'quarter']]

df_demand_index = df_demand.set_index('date_time')

df_final = df_demand.pivot(index='date_time', columns='distributor_code', values='demand_thous')

df_sum_demand_hourly = df_demand.groupby(['date_time'])['demand'].sum().reset_index()

df_sum_demand_hourly['demand_mm'] = df_sum_demand_hourly['demand']/1e6

df_sum_demand_hourly = df_sum_demand_hourly.set_index('date_time')

df_sum_demand_daily = df_demand_index.resample('D').sum().drop(['demand_thous', 'quarter'], axis=1)

df_sum_demand_daily['demand_mm'] = df_sum_demand_daily['demand']/1e6

sns.set(rc={'figure.figsize':(11, 6)})

fig, ax = plt.subplots()# graph with matplotlib
df_final.plot(ax=ax)
plt.gcf().autofmt_xdate()
plt.xticks(fontsize = 12, rotation=90)
plt.yticks(fontsize = 12)
plt.legend(bbox_to_anchor=(1,1), loc="upper left", prop={'size': 10})
plt.xlabel('Date-time', fontsize=12)
plt.ylabel('Energy Demand by operator (KWh)', fontsize=12)
#fig.set_size_inches(6, 3)

#fig1, ax1 =plt.subplots()
#ax1 = df_demand_index['demand_thous'].plot(linewidth=0.5);
#ax1.set_ylabel('Hourly energy demand by operator (KWh)');

fig2, ax2 =plt.subplots()
ax2 = df_demand_index.loc['2010-01-01':'2010-01-15', 'demand_thous'].plot(marker='.', linestyle='-', markersize=2, linewidth=0.5, color='green')
ax2.set_ylabel('Hourly Consumption (KWh)');

fig3, ax3 =plt.subplots()
ax3 = df_demand_index.loc['2010-01-01':'2010-01-15', 'demand_thous'].plot(marker='.', linestyle='None', markersize=2, color='blue')
ax3.set_ylabel('Hourly Consumption (KWh)');

fig4, ax4 =plt.subplots()
ax4 = df_sum_demand_hourly['demand_mm'].plot(linewidth=0.5, color='red', marker='.', markersize=2);
ax4.set_ylabel('Sum of Hourly Energy Demand (GWh)');
ax4.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

fig5, ax5 =plt.subplots()
ax5 = df_sum_demand_daily['demand_mm'].plot(linewidth=0.5, color='orange', marker='.', markersize=2);
ax5.set_ylabel('Sum of Daily Energy Demand (GWh)');
ax5.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
plt.title('Colombia Energy Consumption 2010 (GWh)')


