from numpy.ma.core import count
import pandas as pd
from pandas.core.frame import DataFrame
import constants
import numpy as np
import matplotlib.pyplot as plt

all_data = pd.read_csv(constants.PROJECT_PATH+'/all_data.csv')
all_data.pop(all_data.columns[0])

averages, ones, zeros, nans = [], [], [], []
for column in all_data.columns:
    avg = all_data[column].mean()
    count_ones = len(all_data[all_data[column] == 1])
    count_zeros = len(all_data[all_data[column] == 0])
    count_nans = all_data[column].isna().sum()
    averages.append(avg)
    ones.append(count_ones)
    zeros.append(count_zeros)
    nans.append(count_nans)

column_summary = DataFrame(all_data.columns)
column_summary.columns = ['Indicator']
column_summary['Average'] = averages
column_summary['Ones'] = ones
column_summary['Zeros'] = zeros
column_summary['NAs'] = nans

column_summary.to_csv(constants.PROJECT_PATH+'/indicator_summary.csv', index=False)


zeros, nans = [], []
for index, row in all_data.iterrows():
    count_z = sum(row == 0)
    nas = row.isna().sum()
    zeros.append(count_z)
    nans.append(nas)

all_data['zeros'] = zeros
all_data['NAs'] = nans

half = len(all_data) // 2
all_data_first_half = all_data.iloc[:half,]
all_data_second_half = all_data.iloc[half:]

all_data_first_half.to_csv(constants.PROJECT_PATH+'/all_data_first_half.csv', index=False)
all_data_second_half.to_csv(constants.PROJECT_PATH+'/all_data_second_half.csv', index=False)