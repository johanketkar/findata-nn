import pandas as pd 
import os
import constants

df = pd.read_csv(constants.PROJECT_PATH+'/all_data_first_half.csv')

print(df.head())