mat_lon = df_stn.loc[0:499, 'lon'].values
long_stn = np.repeat(np.reshape(mat_lon, (1, len(mat_lon))), df_merra2.shape[0], axis=0)
long_all = np.reshape(df_merra2['lon'].values, (df_merra2.shape[0], 1))
diff_long2 = (long_stn - long_all) ** 2

mat_lat = df_stn.loc[0:499, 'lat'].values
lat_stn = np.repeat(np.reshape(mat_lat, (1, len(mat_lat))), df_merra2.shape[0], axis=0)
lat_all = np.reshape(df_merra2['lat'].values, (df_merra2.shape[0], 1))
diff_lat2 = (lat_stn - lat_all) ** 2

indices = np.sqrt(diff_lat2 + diff_long2).argmin(axis=0)

test = df_stn.iloc[0:500, :].copy()
test['ref_lat'] = df_merra2.loc[indices, 'lat'].values
test['ref_lon'] = df_merra2.loc[indices, 'lon'].values

np.unique(diff_long2.argmin(axis=0), return_counts=True)

df_merra2.head()
df_stn.head()


'''
def euclidean_distance(df1, df2):  # issue size memory
    dist_temp = pd.DataFrame(np.zeros((3,3)))
    for i in range(3):
        for j in range(3):
            dist_temp.iloc[i, j] = np.sqrt((df2.lat[j] - df1.lat[i]) ** 2 + (df2.lon[j] - df1.lon[i]) ** 2)
            dist_temp['coord'] = '(' + str(df1.lat[i]) + ',' + str(df1.lon[i]) + ')'
            dist_temp = dist_temp.rename({j: df2.area_code[j]}, axis='columns')
            dist = dist_temp.set_index('coord')
            min_stn = pd.DataFrame(dist.idxmin()).reset_index()
            min_stn.columns = ['area_code', 'coord']
    return dist

knn = euclidean_distance(df_merra2, df_stn)
print(knn)
'''