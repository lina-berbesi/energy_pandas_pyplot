#IDEAM Stations
import glob
import pandas as pd
import re
import time
import numpy as np
import matplotlib.pyplot as plt

# Geographical information - where the measurements were taken
area_info = pd.read_excel('CATALOGO_IDEAM_2012-usuarios.xls', sheet_name='Hoja1', index_col=0, nrows=4438)
area_info.shape
print(area_info.columns)
area_info = area_info[
    ['CODIGO', 'LATITUD', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'LONGITUD', 'Unnamed: 17', 'Unnamed: 18',
     'Unnamed: 19']]
area_info['area_code'] = area_info["CODIGO"].astype('str')
area_info['latitude_dms'] = area_info["LATITUD"].astype(str) + "°" + area_info["Unnamed: 13"].astype(str) + "'" + \
                            area_info["Unnamed: 14"].astype(str) + "\"" + area_info["Unnamed: 15"].astype(str)
area_info['longitude_dms'] = area_info["LONGITUD"].astype(str) + "°" + area_info["Unnamed: 17"].astype(str) + "'" + \
                             area_info["Unnamed: 18"].astype(str) + "\"" + area_info["Unnamed: 19"].astype(str)
df_area = area_info[['area_code', 'latitude_dms', 'longitude_dms']]
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

# MULTIPLE POINTS PER MONTH
# Data used: M2TUNXFLX_5.12.4
# M2TUNXFLX: MERRA-2 tavgU_2d_flx_Nx: 2d,diurnal,Time-Averaged,Single-Level,Assimilation,Surface Flux Diagnostics V5.12.4
import netCDF4
from matplotlib import pyplot as plt
import numpy as np
import xarray as xr
import matplotlib.patches as mpatches

# load NetCDF file into variable - using xarray open dataset function
data = xr.open_dataset('MERRA2_300.tavgU_2d_flx_Nx.201001.nc4')

# calculating wind speed
# U2M is 2-meter eastward wind m/s and V2M is 2-meter northward wind m/s

data_new = data
data_new['UVLML'] = (data['ULML'] ** 2 + data['VLML'] ** 2) ** (1 / 2)

data_loc = data_new.sel(lon=14, lat=40, method='nearest')

# plot time series
data_loc['UVLML'].plot.line('o-', color='red', figsize=(10, 6))

# GETTING INFORMATION JUST FROM SPECIFIC COORDINATES

df2_area = df_area.rename({'latitude_dd': 'lat', 'longitude_dd': 'lon'}, axis='columns').drop(
    {'latitude_dms', 'longitude_dms'}, axis='columns')

max_lat = df2_area['lat'].max()
min_lat = df2_area['lat'].min()
max_lon = df2_area['lon'].max()
min_lon = df2_area['lon'].min()
print(max_lat, min_lat, max_lon, min_lon)

print(data_new.sizes)

mask = ((data_new.coords["lat"] > -5) & (data_new.coords["lat"] < 16) & (data_new.coords["lon"] > -82) & (
        data_new.coords["lon"] < 74))

data_sel = data_new.where(mask, drop=True)[['UVLML']]

print(data_sel.sizes)

df_data = data_sel.to_dataframe()

# ONE POINT PER MONTH
# Data used: M2T1NXSLV 5.12.4
# M2IUNXLFO: MERRA-2 instU_2d_lfo_Nx: 2d,diurnal,Instantaneous,Single-Level,Assimilation,Land Surface Forcings V5.12.4
import netCDF4
from matplotlib import pyplot as plt
import numpy as np
import xarray as xr
import matplotlib.patches as mpatches

# load NetCDF file into variable - using xarray open dataset function
data = xr.open_dataset('MERRA2_300.tavgM_2d_slv_Nx.201001.nc4')

# calculating wind speed
# U2M is 2-meter eastward wind m/s and V2M is 2-meter northward wind m/s

data_new = data
data_new['UV2M'] = (data['U2M'] ** 2 + data['V2M'] ** 2) ** (1 / 2)

data_loc = data_new.sel(lon=14, lat=40, method='nearest')

# plot time series
data_loc['UV2M'].plot.line('o-', color='green', figsize=(10, 6))

# GETTING INFORMATION JUST FROM SPECIFIC COORDINATES

df2_area = df_area.rename({'latitude_dd': 'lat', 'longitude_dd': 'lon'}, axis='columns').drop(
    {'latitude_dms', 'longitude_dms'}, axis='columns')

df_stn = df2_area.reset_index().drop(columns=['No. '])

max_lat = df_stn['lat'].max()
min_lat = df_stn['lat'].min()
max_lon = df_stn['lon'].max()
min_lon = df_stn['lon'].min()
print(max_lat, min_lat, max_lon, min_lon)

print(data_new.sizes)

mask = ((data_new.coords["lat"] > -5) & (data_new.coords["lat"] < 16) & (data_new.coords["lon"] > -82) & (
        data_new.coords["lon"] < 74))

data_sel = data_new.where(mask, drop=True)[['UV2M']]

print(data_sel.sizes)

df_data = data_sel.to_dataframe()

df_data.iloc[2,]

df_merra2 = df_data.reset_index()

df_merra2.columns.values

df_merra2.info(memory_usage='deep')  # 280 KB
df_stn.info(memory_usage='deep')  # 334 KB

print(len(df_merra2), len(df_stn))

def chunks(df,n):
    chnk=np.round(np.arange(0, df.shape[0] + df.shape[0]/ n, df.shape[0]/ n)).astype(int)
    return(chnk)

vector = chunks(df_stn, 10)

dist = pd.DataFrame([])

for i in np.arange(len(vector)-1):

    print(vector[i], (vector[i + 1] - 1))

    mat_lon = df_stn.loc[vector[i]:(vector[i + 1] - 1), 'lon'].values
    long_stn = np.repeat(np.reshape(mat_lon, (1, len(mat_lon))), df_merra2.shape[0], axis=0)
    long_all = np.reshape(df_merra2['lon'].values, (df_merra2.shape[0], 1))
    diff_long2 = (long_stn - long_all) ** 2

    mat_lat = df_stn.loc[vector[i]:(vector[i + 1] - 1), 'lat'].values
    lat_stn = np.repeat(np.reshape(mat_lat, (1, len(mat_lat))), df_merra2.shape[0], axis=0)
    lat_all = np.reshape(df_merra2['lat'].values, (df_merra2.shape[0], 1))
    diff_lat2 = (lat_stn - lat_all) ** 2

    indices = np.sqrt(diff_lat2 + diff_long2).argmin(axis=0) # this is not working it is given indices of 6k

    dist_temp = df_stn.iloc[vector[i]:vector[i + 1], :].copy()
    dist_temp['ref_lat'] = df_merra2.loc[indices, 'lat'].values #does not work for the same indices reason from above
    dist_temp['ref_lon'] = df_merra2.loc[indices, 'lon'].values

    dist = dist.append(dist_temp)

dist['ref'] = ['('+ str(i) +','+str(j)+')' for i, j  in zip(dist.ref_lat, dist.ref_lon)]

dist.to_csv('stn_merra2.csv')
