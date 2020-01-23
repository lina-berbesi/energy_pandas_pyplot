import numpy as np
from time import time
import pandas as pd

# Prepare data
np.random.RandomState(100)
arr = np.random.randint(0, 10, size=[200000, 2])
dat = arr.tolist()
dat[:5]

def dummy(a, b):
    return(a + b)
# Parallelizing using Pool.apply()

import multiprocessing as mp
from joblib import Parallel, delayed

# Step 1: Init multiprocessing.Pool()
nodes = mp.cpu_count()

data= pd.DataFrame()

data = data.append(Parallel(n_jobs = nodes)(delayed(dummy)(row[0], row[1]) for row in dat))

# Step 2: `pool.apply` the `howmany_within_range()`
results = [pool.apply(dummy, args=(row[0], row[1])) for row in data]

# Step 3: Don't forget to close
pool.close()

print(results[:10])
#> [3, 1, 4, 4, 4, 2, 1, 1, 3, 3]


from multiprocessing import Pool

def square(x):
    # calculate the square of the value of x
    return x*x

if __name__ == '__main__':

    # Define the dataset
    dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    # Output the dataset
    print ('Dataset: ' + str(dataset))

    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    agents = 3
    chunksize = 3
    with Pool(processes=agents) as pool:
        result = pool.map(square, dataset, chunksize)

    # Output the result
    print ('Result:  ' + str(result))

