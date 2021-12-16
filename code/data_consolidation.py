import pandas as pd
import os
import numpy as np
from constants import CONSOLIDATED_COLUMNS
import constants

#Loop through all ticker folders
#for every quarter at time (t) check to see if that quarter MRQ is covered and if (t-1) MRQ and MRT are covered
#if yes, create data row with columns: good indicators at (t-1) and last column = price(t)
#consolidate all such rows into one dataframe and save as csv
data_path = constants.DATA_PATH
quarter_report_dates = constants.QUARTER_REPORT_DATES
good_indicators = constants.GOOD_INDICATORS

consolidated_df = pd.DataFrame(columns=constants.CONSOLIDATED_COLUMNS)

def is_usable_date(t1, df):
    t1_index = quarter_report_dates.index(t1)
    t0_index = t1_index - 1
    if(t0_index < 0):
        return False, False
    
    t0 = quarter_report_dates[t0_index]

    MRQ_t0 = ((df['dimension'] == 'MRQ') & df[t0] == 1).any()
    MRT_t0 = ((df['dimension'] == 'MRT') & df[t0] == 1).any()
    MRQ_t1 = ((df['dimension'] == 'MRQ') & df[t1] == 1).any()

    return (MRQ_t0 and MRT_t0 and MRQ_t1), t0
      
for ticker in os.listdir(data_path):
    if(ticker == '.DS_Store'):
        continue
    coverage_df = pd.read_csv(data_path+'/'+ticker+'/'+ticker+'_coverage.csv')
    mr_df = pd.read_csv(data_path+'/'+ticker+'/'+ticker+'_mr.csv')

    #for every qaurter report date (t) check to see if that quarter has a price and if the previous quarter (t-1) has MRQ and MRT data
    for t1 in quarter_report_dates:
        is_usable, t0 = is_usable_date(t1, coverage_df)
        if(is_usable):
            #create data row where columns are good indicators at (t-1) and last column = price at (t)
            mrq_t0 = mr_df[((mr_df['dimension'] == 'MRQ') & (mr_df['calendardate'] == t0))]
            mrq_t0 = mrq_t0[good_indicators]
            mrq_t0 = mrq_t0.rename(constants.RENAME_MRQ, axis=1)

            mrt_t0 = mr_df[((mr_df['dimension'] == 'MRT') & (mr_df['calendardate'] == t0))]
            mrt_t0 = mrt_t0[good_indicators]
            mrt_t0 = mrt_t0.rename(constants.RENAME_MRT, axis=1)

            price_t1 = mr_df[((mr_df['dimension'] == 'MRQ') & (mr_df['calendardate'] == t1))]['price'].values
            price_df = pd.DataFrame()
            price_df['price_t'] = price_t1
            price_df['ticker'] = ticker

            new_row = pd.merge(mrq_t0, mrt_t0)
            new_row = pd.merge(new_row, price_df)
            new_row.pop('ticker')

            consolidated_df = consolidated_df.append(new_row)

consolidated_df.to_csv(constants.PROJECT_PATH+'/all_data.csv')

