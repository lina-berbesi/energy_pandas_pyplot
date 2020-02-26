#conda install --name Thesis netcdf4
#conda install --name Thesis cartopy
#conda install --name Thesis ncdump
# Database MERRA2: https://disc.gsfc.nasa.gov/datasets/M2TMNXSLV_5.12.4/summary?keywords=M2TMNXSLV_5.12.4

### EXAMPLE WIND PLOTTING:
#https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20calculate%20and%20plot%20wind%20speed%20using%20MERRA-2%20wind%20component%20data%20using%20Python

#PLOT MERRA-2 WIND SPEED

# The NetCDF4 Dataset and numpy imports allow you to read in the file and perform calculations.

from netCDF4 import Dataset
import numpy as np
#data = Dataset('MERRA2\M2T1NXSLV\MERRA2_300.tavg1_2d_slv_Nx.20100601.nc4', mode='r')
data = Dataset('MERRA2\M2TMNXSLV\MERRA2_300.tavgM_2d_slv_Nx.201001.nc4', mode = 'r')

# Run the following cell to see the MERRA2 metadata. This line will print attribute and variable information. From the 'variables(dimensions)' list, choose which variable(s) to read in below:
print(data)

# Read in variables:

lons = data.variables['lon']
lats = data.variables['lat']

# 2-meter eastward wind m/s
U2M = data.variables['U2M']

# 2-meter northward wind m/s
V2M = data.variables['V2M']
time = data.variables['time']

# Replace _FillValues with NaNs:
U2M_nans = U2M[:]
V2M_nans = V2M[:]
_FillValueU2M = U2M._FillValue
_FillValueV2M = V2M._FillValue
U2M_nans[U2M_nans == _FillValueU2M] = np.nan
V2M_nans[V2M_nans == _FillValueV2M] = np.nan

# Compute wind speeds:

ws = np.sqrt(U2M_nans**2+V2M_nans**2)

# Wind speed directions in radians:

ws_direction = np.arctan2(V2M_nans,U2M_nans)

# NOTE: the MERRA-2 file contains hourly data for 24 hours (t=24), so we must take the average along the time dimension

# Compute daily average wind speed:
ws_daily_avg = np.nanmean(ws, axis=0)

# Daily average wind speed direction in radians:

ws_daily_avg_direction = np.nanmean(ws_direction, axis=0)

#Plot Global MERRA-2 Wind Speed: with the wind coordenates

#conda install --name Thesis mpl_toolkits
# The matplotlib and Basemap libraries allow you to plot the data:
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

# Map the data onto the base map and add features:
#you have to close any map window if you have one
map = Basemap(resolution='l', projection='eck4', lat_0=0, lon_0=0)

lon, lat = np.meshgrid(lons, lats)
xi, yi = map(lon, lat)

# Plot windspeed:
cs = map.pcolor(xi,yi,ws[0,:,:], vmin=0, vmax=12, cmap=cm.rainbow)
cs.set_edgecolor('face')


# Add grid lines:
map.drawparallels(np.arange(-90., 90., 15.), labels=[1,0,0,0], fontsize=4, linewidth=0.5)
map.drawmeridians(np.arange(-180., 180., 30.), labels=[0,0,0,1], fontsize=4, linewidth=0.5)

# Add coastlines, states, and country boundaries:

map.drawcoastlines(color='k', linewidth=0.25)

map.drawstates(color='k', linewidth=0.25)
map.drawcountries(color='k', linewidth=0.25)

# Add colorbar:
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('m/s')
cbar.ax.tick_params(labelsize=8)

# Add title:
from textwrap import wrap
plt.title("\n".join(wrap('Hourly MERRA-2 calculated 2-meter wind speed (m/s) (2010-01-01T00:00:00)')), fontsize=10)

figure1 = plt.figure(1)

# Save figure as PNG:
figure1.savefig('MERRA2_2m_ws.png', format='png', dpi=360)

# Plot Wind Speed With Direction

# Note that the "quiver" function uses arrows to show the wind direction (not wind magnitude):

map = Basemap(width=2500000,height=2000000,
            resolution='l',projection='stere',\
            lat_ts=50,lat_0=48,lon_0=-50)

lon, lat = np.meshgrid(lons, lats)
xi, yi = map(lon, lat)


# Plot wind speed and direction:

cs = map.pcolor(xi,yi,ws[0,:,:], vmin=0, vmax=12, cmap=cm.rainbow)
cs.set_edgecolor('face')
map.quiver(xi, yi, U2M_nans[0,:,:], V2M_nans[0,:,:], scale=400, color='k')


# Add grid lines:
map.drawparallels(np.arange(30, 70, 5), labels=[1,0,0,0], fontsize=4, linewidth=0.3)
map.drawmeridians(np.arange(-180., 180., 10), labels=[0,0,0,1], fontsize=4, linewidth=0.3)

# Add coastlines, states, and country boundaries:
map.drawcoastlines(color='k', linewidth=0.5)
map.drawstates(color='k', linewidth=0.5)
map.drawcountries(color='k', linewidth=0.5)

# Add colorbar:
cbar = map.colorbar(cs, location='bottom', pad="5%")
cbar.set_label('m/s')
cbar.ax.tick_params(labelsize=8)

# Add title:
from textwrap import wrap
plt.title("\n".join(wrap('Hourly MERRA-2 calculated 2-meter wind speed (m/s) with direction (2010-01-01T00:00:00)')), fontsize=10)

figure2 = plt.figure(1)

# Save figure as PNG:
figure2.savefig('MERRA2_2m_wsVECTORS.png', format='png', dpi=360)

### EXAMPLE HOW TO PLOT AIR TEMPERATURE:
# https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20read%20and%20plot%20NetCDF%20MERRA-2%20data%20in%20Python

#Checking tables

# Import the required Python libraries. They are used to read and plot the data. If any of the following import commands fail, check the local Python environment and install any missing packages.

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os

# Read in NetCDF4 file (add a directory path if necessary):

#data = Dataset('MERRA2\M2IUNXLFO\MERRA2_400.instU_2d_lfo_Nx.201901.nc4', mode='r')
data = Dataset('MERRA2\M2TMNXSLV\MERRA2_300.tavgM_2d_slv_Nx.201001.nc4', mode='r')

# Run the following line below to print MERRA-2 metadata. This line will print attribute and variable information. From the 'variables(dimensions)' list, choose which variable(s) to read in below.
print(data)

# Read in the 'T2M' 2-meter air temperature variable:
lons = data.variables['lon'][:]
lats = data.variables['lat'][:]
T2M = data.variables['T2M'][:, :, :]

# If using MERRA-2 data with multiple time indices in the file, the following line will extract only the first time index.
# Note: Changing T2M[0,:,:] to T2M[10,:,:] will subset to the 11th time index.

#2 meter air temperature
T2M = T2M[0, :, :]

# Plot the data using matplotlib and cartopy

# Set the figure size, projection, and extent
fig = plt.figure(figsize=(8, 4))
ax = plt.axes(projection=ccrs.Robinson())
ax.set_global()
ax.coastlines(resolution="110m", linewidth=1)
ax.gridlines(linestyle='--', color='black')

# Set contour levels, then draw the plot and a colorbar
clevs = np.arange(230, 311, 5)
plt.contourf(lons, lats, T2M, clevs, transform=ccrs.PlateCarree(), cmap=plt.cm.jet)
plt.title('MERRA-2 Air Temperature at 2m, January 2010', size=14)
cb = plt.colorbar(ax=ax, orientation="vertical", pad=0.02, aspect=16, shrink=0.8)
cb.set_label('K', size=12, rotation=0, labelpad=15)
cb.ax.tick_params(labelsize=10)

# Save the plot as a PNG image

fig.savefig('MERRA2_t2m.png', format='png', dpi=360)



#it didnt work data access: https://disc.gsfc.nasa.gov/data-access#python-pydap

import pandas as pd

from pydap.client import open_url
from pydap.cas.urs import setup_session

dataset_url = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2_DIURNAL/M2IUNXLFO.5.12.4/M2IUNXLFO_5.12.4_dif.xml'
session = setup_session(lber562, Rojas891, check_url=dataset_url)
dataset = open_url(dataset_url, session=session)