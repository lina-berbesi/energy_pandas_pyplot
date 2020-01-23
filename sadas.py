import pandas as pd
import numpy as np
test = pd.DataFrame(data = np.reshape(np.arange(0, 10), (5,2)), columns = ['uno', 'dos'])

mock = test.copy()
for i in np.arange(10):
    temp = test.rename(columns = {'uno':str(i)})
    mock = pd.concat([mock, temp], axis = 1)