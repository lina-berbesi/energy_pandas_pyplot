import glob
import pandas as pd
import re
import time
import numpy as np
import matplotlib.pyplot as plt
import astropy
from astropy.io import ascii

###New Information

data = ascii.read('20199050103532mensual.txt', delimiter='\t', format='no_header', names=['Year','Stat','Ent','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'], data_start=16, data_end=20, guess=False, fast_reader=False)

data = ascii.read('20199050103532mensual.txt', delimiter='\t', format='no_header', data_start=16, data_end=20, guess=False, fast_reader=False)
print(data)

data = ascii.read('20199050103532mensual.txt', format='fixed_width', header_start=8, data_start=10,  data_end=52, guess=False, fast_reader=False)
print(data)

data = ascii.read('20199050103532mensual.txt', format='basic', delimiter='\t', guess='False', fast_reader='False')
print(data)

data = ascii.read('20199050103532mensual.txt', format='tab', guess='False', fast_reader='False')
print(data)

data.info

# Open file
f = open('20199050103532mensual.txt', 'r')
# Read and ignore header lines
header1 = f.readline()
header2 = f.readline()
header3 = f.readline() #variable
header4 = f.readline()
#This is where the station information starts
header5 = f.readline() #Date - Station Number
header6 = f.readline() #empty space
header7 = f.readline() #Latitude
header8 = f.readline() #longitude
header9 = f.readline() #Altitude
header10 = f.readline() #empty space
header11 = f.readline() #*
header12 = f.readline() #titles
header13 = f.readline() #*
header14 = f.readline() #empty space
header15 = f.readline() #empty space
header16 = f.readline() #empty space
# Loop over lines and extract variables of interest
data = []
for line in f:
    line = line.strip()
    columns = line.split()
    print(line,columns)
    if "I D E A M" in line:
        break

f.close()

trial = pd.read_txt('20199050103532mensual.txt') # does not work
trial2 = pd.read_csv('20199050103532mensual.txt', sep='\t', lineterminator='\n')
print(trial2.head(20))