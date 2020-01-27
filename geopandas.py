#conda install --name geopandas matplotlib
import pandas as pd
import geopandas as gpd
import os
import matplotlib
import descartes
import matplotlib.pyplot as plt
import fiona; help(fiona.open)
from shapely.geometry import Point,Polygon

###Geopandas

os.getcwd()

# Set filepath (fix path relative to yours)
fp = "C:/Users/linab/PycharmProjects/geopandas/MGN2018_00_COLOMBIA/WGS84_MGN2019_00_COLOMBIA/ADMINISTRATIVO/MGN_DPTO_POLITICO.shp"

# Read file using gpd.read_file()
data = gpd.read_file(fp)

data.head()

#reading pts for stations
df = pd.read_csv('stn_merra2.csv')

df_ideam = df.drop(['Unnamed: 0','ref_lon','ref_lat'],axis=1)

df_merra2 = df.drop(['Unnamed: 0','lon','lat'],axis=1)

df['status'].value_counts()

crs={'init': 'epsg:4326'}

geom_ideam = [Point(xy) for xy in zip(df_ideam["lon"], df_ideam["lat"])]
geom_merra2 = [Point(xy) for xy in zip(df_merra2["ref_lon"], df_merra2["ref_lat"])]

gdf_ideam = gpd.GeoDataFrame(df_ideam, crs=crs, geometry=geom_ideam)

gdf_merra2 = gpd.GeoDataFrame(df_merra2, crs=crs, geometry=geom_merra2)

#plotting the stations in the map
fig, ax = plt.subplots(figsize=(5,5))

data.plot(ax=ax, color='silver',zorder=1)

gdf_ideam.plot(ax=ax, color='red',markersize=2,zorder=2)

gdf_merra2.plot(ax=ax, color='blue',markersize=2,zorder=2)

gdf_ideam[gdf_ideam.status == 'ACT'].plot(ax=ax, color='green',markersize=2,zorder=2)

plt.show()

