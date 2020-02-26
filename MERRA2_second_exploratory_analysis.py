#Daily information of the month

#M2I1NXASM: MERRA-2 inst1_2d_asm_Nx: 2d,1-Hourly,Instantaneous,Single-Level,Assimilation,Single-Level Diagnostics V5.12.4

import netCDF4
from matplotlib import pyplot as plt
import numpy as np
import xarray as xr
import matplotlib.patches as mpatches
import glob
import pandas as pd

filenames_xasm = glob.glob('MERRA2/M2I1NXASM/MERRA2_400.inst1_2d_asm_Nx'+'*.{}'.format('nc'))

df_xasm = pd.DataFrame()
for f in filenames_xasm:
    data_xasm = xr.open_dataset(f)
    df_data_xasm = data_xasm.to_dataframe()
    df_n_xasm = df_data_xasm.reset_index()
    df_n_xasm['UV2M'] = (df_n_xasm['U2M'] ** 2 + df_n_xasm['V2M'] ** 2) ** (1 / 2)
    df_xasm = pd.concat([df_xasm, df_n_xasm], axis=0)

print(df_xasm['time'].unique())
print(df_xasm.columns)

df_mean_xasm = df_xasm.groupby(['time'])['UV2M'].mean().reset_index()

#M2T1NXSLV: MERRA-2 tavg1_2d_slv_Nx: 2d,1-Hourly,Time-Averaged,Single-Level,Assimilation,Single-Level Diagnostics V5.12.4

import netCDF4
from matplotlib import pyplot as plt
import numpy as np
import xarray as xr
import matplotlib.patches as mpatches
import glob
import pandas as pd

filenames_xslv = glob.glob('MERRA2/M2T1NXSLV/MERRA2_400.tavg1_2d_slv_Nx.'+'*.{}'.format('nc'))

df_xslv = pd.DataFrame()
for f in filenames_xslv:
    data_xslv = xr.open_dataset(f)
    df_data_xslv = data_xslv.to_dataframe()
    df_n_xslv = df_data_xslv.reset_index()
    df_n_xslv['UV2M'] = (df_n_xslv['U2M'] ** 2 + df_n_xslv['V2M'] ** 2) ** (1 / 2)
    df_xslv = pd.concat([df_xslv, df_n_xslv], axis=0)

print(df_xslv['time'].unique())
print(df_xslv.columns)

df_mean_xslv = df_xslv.groupby(['time'])['UV2M'].mean().reset_index()

fig9, ax9 = plt.subplots()
df_mean_xasm.plot(x='time', y='UV2M', kind='line', color='blue', grid=True, label ='UV2M-XASM', ax=ax9)

fig10, ax10 = plt.subplots()
df_mean_xslv.plot(x='time', y='UV2M', kind='line', color='green', grid=True, label='UV2M-XSLV', ax=ax10)

