import os
import pandas as pd 
import numpy as np

PROJECT_PATH = os.path.dirname(os.getcwd())
DATA_PATH = os.path.join(PROJECT_PATH, 'data')


ALL_YEARS = [1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
             2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]
Q1_REPORT_MONTH_DAY_STRING = '03-31'
Q2_REPORT_MONTH_DAY_STRING = '06-30'
Q3_REPORT_MONTH_DAY_STRING = '09-30'
Q4_REPORT_MONTH_DAY_STRING = '12-31'
ANNUAL_REPORT_MONTH_DAY_STRING = '12-31'

quarter_report_dates = []
for year in ALL_YEARS:
    q1 = str(year) + '-' + Q1_REPORT_MONTH_DAY_STRING
    q2 = str(year) + '-' + Q2_REPORT_MONTH_DAY_STRING
    q3 = str(year) + '-' + Q3_REPORT_MONTH_DAY_STRING
    q4 = str(year) + '-' + Q4_REPORT_MONTH_DAY_STRING
    quarter_report_dates.append(q1)
    quarter_report_dates.append(q2)
    quarter_report_dates.append(q3)
    quarter_report_dates.append(q4)

QUARTER_REPORT_DATES = quarter_report_dates

indicator_coverage_df = pd.read_csv(PROJECT_PATH+'/indicator_coverage.csv')
all_indicators_list = indicator_coverage_df.columns.tolist()
all_indicators_list.pop(0)
INDICATORS = all_indicators_list

good_indicator_list = []
for indicator in all_indicators_list:
    percent_covered = indicator_coverage_df[indicator][0]
    if percent_covered > .90:
        good_indicator_list.append(indicator)

good_indicator_list.append('ticker')

GOOD_INDICATORS = good_indicator_list

rename_MRQ = {}
rename_MRT = {}
consolidated_column_names = []
for indicator in good_indicator_list:
    if(indicator== 'ticker'):
        continue
    mrq = indicator+'_mrq'
    mrt = indicator+'_mrt'
    rename_MRQ[indicator] = mrq
    rename_MRT[indicator] = mrt
    consolidated_column_names.append(mrq)
    consolidated_column_names.append(mrt)

consolidated_column_names.append('price_t')
RENAME_MRQ = rename_MRQ
RENAME_MRT = rename_MRT
CONSOLIDATED_COLUMNS = consolidated_column_names
