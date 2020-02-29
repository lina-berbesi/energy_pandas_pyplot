#IDEAM Stations
import glob
import pandas as pd
import re
import time
import numpy as np
import matplotlib.pyplot as plt

# Geographical information - where the measurements were taken
area_info = pd.read_excel('IDEAM\CATALOGO_IDEAM_2012-usuarios.xls', sheet_name='Hoja1', index_col=0, nrows=4438)
area_info.shape
print(area_info.columns)
area_info = area_info[
    ['CODIGO', 'LATITUD', 'ESTADO', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'LONGITUD', 'Unnamed: 17', 'Unnamed: 18',
     'Unnamed: 19']]
area_info['area_code'] = area_info["CODIGO"].astype('str')
area_info['status'] = area_info["ESTADO"].astype('str')
area_info['latitude_dms'] = area_info["LATITUD"].astype(str) + "°" + area_info["Unnamed: 13"].astype(str) + "'" + \
                            area_info["Unnamed: 14"].astype(str) + "\"" + area_info["Unnamed: 15"].astype(str)
area_info['longitude_dms'] = area_info["LONGITUD"].astype(str) + "°" + area_info["Unnamed: 17"].astype(str) + "'" + \
                             area_info["Unnamed: 18"].astype(str) + "\"" + area_info["Unnamed: 19"].astype(str)
df_area = area_info[['area_code','status', 'latitude_dms', 'longitude_dms']]
df_area['area_code'] = area_info["area_code"].astype('category')
print(df_area.head(5))
print(df_area.dtypes)

# Convert DMS to DD
def dms_dd(dms):
    parts = re.split('[°\'"]+', dms)
    de = float(parts[0])
    mi = float(parts[1])
    se = float(parts[2])
    dr = parts[3]
    dd = de + mi / 60 + se / (60 * 60)
    if dr == 'S' or dr == 'W':
        dd *= -1
    return dd;

df_area['latitude_dd'] = df_area['latitude_dms'].apply(dms_dd)
df_area['longitude_dd'] = df_area['longitude_dms'].apply(dms_dd)
df_area.head(5)
print(df_area.dtypes)

# DatabaseMERRA2:https://disc.gsfc.nasa.gov/datasets/M2TMNXSLV_5.12.4/summary?keywords=M2TMNXSLV_5.12.4
# Example of plotting time series: https://www.wemcouncil.org/wp/wemc-tech-blog-2-plotting-netcdf-with-python/

# ONE POINT PER MONTH
# Data used: M2TMNXSLV 5.12.4
# M2TMNXSLV: MERRA-2 tavgM_2d_slv_Nx: 2d,Monthly mean,Time-Averaged,Single-Level,Assimilation,Single-Level Diagnostics V5.12.4
import netCDF4
from matplotlib import pyplot as plt
import numpy as np
import xarray as xr
import matplotlib.patches as mpatches
import glob
import datetime as dt
import pandas as pd

#read MERRA2 files in loop

filenames1 = glob.glob('MERRA2\M2TMNXSLV\MERRA2_300.tavgM*.{}'.format('nc4'))
filenames2 = glob.glob('MERRA2\M2TMNXSLV\MERRA2_400.tavgM*.{}'.format('nc4'))
filenames = filenames1 + filenames2
print(filenames)
df_mrr2 = pd.DataFrame()
for f in filenames:
    data = xr.open_dataset(f) # load NetCDF file into variable - using xarray open dataset function
    data_new = data
    data_new['UV2M'] = (data['U2M'] ** 2 + data['V2M'] ** 2) ** (1 / 2) # calculating wind speed # U2M is 2-meter eastward wind m/s and V2M is 2-meter northward wind m/s
    data_new['UV10M'] = (data['U10M'] ** 2 + data['V10M'] ** 2) ** (1 / 2)
    mask = ((data_new.coords["lat"] > -5) & (data_new.coords["lat"] < 16) & (data_new.coords["lon"] > -82) & (data_new.coords["lon"] < 74))
    data_sel = data_new.where(mask, drop=True)[['UV2M', 'UV10M']] #indexing x-array
    df_data = data_sel.to_dataframe()
    df_merra2 = df_data.reset_index()
    df_mrr2 = pd.concat([df_mrr2, df_merra2], axis=0)

df_mrr2["date"] = pd.to_datetime(df_mrr2['time']).dt.date

#read IDEAM files
#'VVAG_MEDIA_M','Average Wind Speed', 'm/s'

df_ideam = pd.read_csv('IDEAM\ideam_data.csv')

df_ideam = df_ideam.filter(['date','area_code','VVAG_MEDIA_M','latitude_dd','longitude_dd'])

print(df_ideam['date'].unique().tolist())

df_ideam['date'] = pd.to_datetime(df_ideam['date']).dt.date

print(df_ideam['date'].unique().tolist())

df_ideam['month'] = df_ideam['date'].values.astype('datetime64[M]')

#Second review of years
df_ideam_final = df_ideam[['month','area_code','VVAG_MEDIA_M','latitude_dd','longitude_dd']]

year19 = df_ideam_final[df_ideam_final['month'].dt.year == 2019]

year19 = year19[year19.VVAG_MEDIA_M.notnull()]

print(len(year19))

year14 = df_ideam_final[df_ideam_final['month'].dt.year == 2014]

year14 = year14[year14.VVAG_MEDIA_M.notnull()]

print(len(year14))

year18 = df_ideam_final[df_ideam_final['month'].dt.year == 2019]

year18 = year18[year18.VVAG_MEDIA_M.notnull()]

print(len(year18))

#Plot

mean_ideam = df_ideam.groupby('month').mean().drop(['area_code','latitude_dd','longitude_dd'],axis=1).reset_index().rename(columns={'month': 'date'})
mean_ideam.set_index('date')
mean_merra2 = df_mrr2.groupby('date').mean().drop(['lat','lon'],axis=1).reset_index()

fig6, ax6 = plt.subplots()
mean_ideam.plot(y='VVAG_MEDIA_M', x='date', color='blue', grid=True, ax=ax6)
ax6.set_title('IDEAM')

fig7, ax7 = plt.subplots()
mean_merra2.plot(y='UV2M', x='date', color='red', grid=True, ax=ax7)
ax7.set_title('MERRA2')

ax8=plt.subplot()
ax8.plot(mean_ideam.date, mean_ideam.VVAG_MEDIA_M,label='Ideam-Local Data')
ax8.plot(mean_merra2.date, mean_merra2.UV2M,label='Merra2-Nasa (2 meter)')
ax8.plot(mean_merra2.date, mean_merra2.UV10M,label='Merra2-Nasa (10 meter)')
ax8.set_title('Monthly Wind Comparison between IDEAM and MERRA2')
plt.show()
plt.legend()











