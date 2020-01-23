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

def chunks(df, n):
    chks_str = []
    chks_end = []
    chks_fnl = []
    ic = 0
    cnt = -1
    while ic < len(df):
        cnt = cnt + 1
        cnt_prev = cnt - 1
        ic = n + ic
        if cnt == 0:
            pv = 0
            chks_end.append(n)
            chks_str.append(0)
            chks_fnl.append(str(chks_str).strip('[]')+':'+str(chks_end).strip('[]'))
        elif ic > len(df):
            ic = len(df)
            chks_end.append(ic)
            chks_str.append(chks_end[cnt_prev])
            chks_fnl.append(str(chks_str[cnt]).strip('[]')+':'+str(chks_end[cnt]).strip('[]'))
        else:
            chks_end.append(ic)
            chks_str.append(chks_end[cnt_prev])
            chks_fnl.append(str(chks_str[cnt]).strip('[]')+':'+str(chks_end[cnt]).strip('[]'))
    return chks_str, chks_end, chks_fnl

chks_stn_str,chks_stn_end,chks_stn_fnl = chunks(df_stn, 500)
print(chks_stn_str,chks_stn_end, chks_stn_fnl)

n1_str=chks_stn_str[i]
n1_end=chks_stn_end[i]

def euclidean_distance(df1, df2, n1_str , n1_end, n2_str, n2_end):  # issue size memory
    dist_temp = pd.DataFrame(np.zeros(((n1_end - n1_str),(n2_end-n2_str))))
    for i in range(n1_str,n1_end):
        for j in range(n2_str,n2_end):
            dist_temp.iloc[i, j] = np.sqrt((df2.lat[j] - df1.lat[i]) ** 2 + (df2.lon[j] - df1.lon[i]) ** 2)
            dist_temp['coord'] = '(' + str(df1.lat[i]) + ',' + str(df1.lon[i]) + ')'
            dist_temp = dist_temp.rename({j: df2.area_code[j]}, axis='columns')
            dist = dist_temp.set_index('coord')
            min_stn = pd.DataFrame(dist.idxmin()).reset_index()
            min_stn.columns = ['area_code', 'coord']
    return min_stn

knn = euclidean_distance(df_merra2, df_stn)
print(knn)

for i in range(0,len(chks_stn_str)):
    print(chks_stn_str[i],chks_stn_end[i])

    mat_lon = df_stn.loc[chks_stn_str[i]:chks_stn_end[i], 'lon'].values
    long_stn = np.repeat(np.reshape(mat_lon, (1, len(mat_lon))), df_merra2.shape[0], axis=0)
    long_all = np.reshape(df_merra2['lon'].values, (df_merra2.shape[0], 1))
    diff_long2 = (long_stn - long_all) ** 2

    mat_lat = df_stn.loc[chks_stn_str[i]:chks_stn_end[i], 'lat'].values
    lat_stn = np.repeat(np.reshape(mat_lat, (1, len(mat_lat))), df_merra2.shape[0], axis=0)
    lat_all = np.reshape(df_merra2['lat'].values, (df_merra2.shape[0], 1))
    diff_lat2 = (lat_stn - lat_all) ** 2

    indices = np.sqrt(diff_lat2 + diff_long2).argmin(axis=0) # this is not working it is given indices of 6k

    test = df_stn.iloc[chks_stn_str[i]:chks_stn_end[i], :].copy()
    test['ref_lat'] = df_merra2.loc[indices, 'lat'].values #does not work for the same indices reason from above
    test['ref_lon'] = df_merra2.loc[indices, 'lon'].values



