'''
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
        elif ic > len(df):
            ic = len(df)
            chks_end.append(ic)
            chks_str.append(chks_end[cnt_prev])
        else:
            chks_end.append(ic)
            chks_str.append(chks_end[cnt_prev])
    return chks_str, chks_end, chks_fnl

chks_stn_str,chks_stn_end= chunks(df_stn, 500)
print(chks_stn_str,chks_stn_end)

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







