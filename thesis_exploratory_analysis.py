#conda install --name myenv scipy
#conda install --name Thesis astropy
import glob
import pandas as pd
import re
import time
import numpy as np
import matplotlib.pyplot as plt

###Previous Information

# Geographical information - where the measurements were taken
area_info = pd.read_excel('IDEAM\CATALOGO_IDEAM_2012-usuarios.xls', sheet_name='Hoja1', index_col=0, nrows=4438)
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


# Variables information - measurements
#Looping over variables

df_var = pd.DataFrame()
variables = ['BSHG_TT_M', 'VVAG_MEDIA_M', 'VVMX_MX_M', 'DVMXAG_MX_M']
for i in variables:
    filenames = glob.glob('IDEAM/' + str(i) + '*.{}'.format('data'))
    df = pd.DataFrame()
    for f in filenames:
        df_n = pd.read_csv(f)
        area = re.sub(r'\@(.*[^\/]+)\.data', '', f) #area = re.sub(r'\@(.*)\.data', '', f) #area = re.sub(r'.data|(\w+@)', '', f)
        var = re.search(r'\w+[^@]', f)
        new = df_n["Fecha|Valor"].str.split("|", n=1, expand=True)
        df_n["date"] = pd.to_datetime(new[0])
        df_n["area_code"] = area
        df_n["area_code"] = df_n["area_code"].astype('category')
        df_n[var.group()] = pd.to_numeric(new[1])
        df_n.drop(columns=["Fecha|Valor"], inplace=True)
        df = pd.concat([df, df_n], axis=0)
        #df.set_index(['date', 'area_code'])
    if df_var.empty == True:
        df_var = df
        #df_final.set_index(['date', 'area_code'])
    else:
        df_var = pd.merge(df_var, df, on=['date', 'area_code'], how='outer')
df_var = df_var.sort_values(['date','area_code'], ascending=[True,True])
print(df_var.columns)
print(df_var.dtypes)
print(df_var.tail(5))
df_var.date.unique()

#Checking max and min dates

maxdat = df_var['date'].max()
mindat = df_var['date'].min()
print(maxdat, mindat)

# Joining of the between GI and Var
df_join = pd.merge(df_var, df_area, on='area_code', how='inner')
df_join.head(5)

df_join.shape

df_join.to_csv('IDEAM\ideam_data.csv')

#Table with variable meaning
data_rows = [('BSHG_TT_M','Sun Intensity','hours/sun'),
             ('VVAG_MEDIA_M','Average Wind Speed', 'm/s'),
             ('VVMX_MX_M','Maximum Wind Speed', 'm/s'),
             ('DVMXAG_MX_M','Maximum Wind Speed', 'degrees')]
df_plot = pd.DataFrame(data_rows,columns=['var','desc','units'])
print(df_plot)

for j in range(2, 6):
    vars = df_var.columns.values[j]
    print(vars)
    desc = df_plot.loc[df_plot['var'] == vars, 'desc'].values[0]
    unit = df_plot.loc[df_plot['var'] == vars, 'units'].values[0]
    print(vars, desc, unit)
    #Graphs
    df_join.plot(x="date",y=vars)
    plt.show()
    plt.title(str(vars)+': '+str(desc))
    plt.xlabel('Date')
    plt.ylabel(str(desc)+' '+str(unit))

#start = time.time()
#end = time.time()
#print("Time with concat")
#print(end - start)

data = df_var[df_var.columns.tolist()[:3]]

for key, grp in data.groupby(['area_code']):
    plt.plot(grp['BSHG_TT_M'], label = "Sun Int in".format(key))
plt.legend(loc='best')
plt.show()


fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])

for i in df_var['area_code'].unique():
    print(i)
    ax.plot(df_var.loc[df_var['area_code'] == i, 'BSHG_TT_M'], label=i)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

plt.title('BSHG_TT_M: Sun Intensity hours/sun per station')

plt.show()



