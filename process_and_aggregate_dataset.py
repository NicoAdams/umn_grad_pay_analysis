''' Run this file to process & aggregate the pay snapshot files in the UMNTC_95XX_pay_data directory
Generates the following new files:
- dfGrad: Combination of all snapshot files, limited to graduate assistants only
- dfGradGrouped: Aggregated dataset, one row per (graduate employee ID, snapshot date) pair. Sums all sources of support for each student at a given time
- dfDeptSplit: Same as dfGradGrouped, but creates a distinct row for each department that is paying each student. (Still keeps track of that student's *total* pay from all sources)
	- This lets us track the *total* pay of students who receive *any* funding from a given department. (Helpful for departments whose students are often paid from a different department)
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

from collections import Counter


# -- 1. Loads the snapshots --
print('Loading and processing snapshots...')

# Loads and processes the list of snapshot datasets

months = ['Jul', 'Oct', 'Mar'] * 7
years = ['2015']*2 + ['2016']*3 + ['2017']*3 + ['2018']*3 + ['2019']*3 + ['2020']*3 + ['2021']*3 + ['2022']
dateStrs = ['15 %s %s' % (months[i], years[i]) for i in range(len(months))]

filenames = [('UMNTC_95XX_pay_data/UMNTC 95XX all, %s.csv'%dateStr) for dateStr in dateStrs]

dfList = [pd.read_csv(f) for f in filenames]

# Forms one large dataframe from the list of snapshots
dfAll = pd.concat(dfList)

# Anonymizes the dataset: Removes "Emplid", "First", and "Last", and replaces them with a random number
emplids = set(dfAll['Emplid'].values)
emplid2AnonymizedID = {emplid: idx for idx, emplid in enumerate(emplids)}
dfAll['Emplid_Anon'] = [emplid2AnonymizedID[emplid] for emplid in dfAll['Emplid'].values]
dfAll = dfAll.drop(columns=['First Name', 'Last Name', 'Emplid'])

# Adds additional utility columns
dfAll['emplid_anon + snapshot'] = [str(emplid)+','+str(date) for (emplid, date) in zip(dfAll['Emplid_Anon'].values, dfAll['Day Date'].values)]

# Limits to graduate assistants only (removes fellows, postdocs, professional students)
dfGrad = dfAll[dfAll['Empl Class'] == 'Graduate Assistants'].copy()


# -- 2. Aggregates by graduate student & date --
print('Aggregating by (emplid, date)...')

# Creates a "grad grouped" dataset, which sums all sources of support for each (emplid, date) pair

aggDict = {
    'Date': pd.NamedAgg(column='Day Date', aggfunc='first'),
    'Emplid_Anon': pd.NamedAgg(column='Emplid_Anon', aggfunc='first'),
    'Hours_total': pd.NamedAgg(column="Standard Hours", aggfunc=sum),
    'Hours_list': pd.NamedAgg(column="Standard Hours", aggfunc=list),
    'Hourly_rate_list': pd.NamedAgg(column='Normalized Hourly Base Rate', aggfunc=list),
    'Annual_P09_list': pd.NamedAgg(column='Calculated Annual P09', aggfunc=list),
    'Annual_P12_list': pd.NamedAgg(column='Calculated Annual P12', aggfunc=list),
    'Department_list': pd.NamedAgg(column='Department', aggfunc=list),
    'College_list': pd.NamedAgg(column='College/Admin Unit', aggfunc=list)
}
dfGradGrouped = dfGrad.groupby('emplid_anon + snapshot').aggregate(**aggDict)

# Computes "effective pay" columns under different conditions

dfGradGrouped['Num_appts'] = [len(l) for l in dfGradGrouped['Hours_list'].values]

dfGradGrouped['Yearly_pay_total_no_summer'] = [
    np.sum([
        row['Annual_P09_list'][i] * row['Hours_list'][i]/40 for i in range(row['Num_appts'])
    ]) for (rowIdx, row) in dfGradGrouped.iterrows()
]
dfGradGrouped['Yearly_pay_total_with_summer'] = [
    np.sum([
        row['Annual_P12_list'][i] * row['Hours_list'][i]/40 for i in range(row['Num_appts'])
    ]) for (rowIdx, row) in dfGradGrouped.iterrows()
]
dfGradGrouped['Eff_hourly_wage_20hr'] = [
    np.sum([
        row['Hourly_rate_list'][i] * row['Hours_list'][i]/20 for i in range(row['Num_appts'])
    ]) for (rowIdx, row) in dfGradGrouped.iterrows()
]
dfGradGrouped['Eff_hourly_wage_40hr'] = [
    np.sum([
        row['Hourly_rate_list'][i] * row['Hours_list'][i]/40 for i in range(row['Num_appts'])
    ]) for (rowIdx, row) in dfGradGrouped.iterrows()
]


# -- 3. Creates a different row for each department that a student is funded from --
print('Splitting by department...')

deptSplitRowDicts = []

# Need to remove all columns with lists in them
colsToKeep = [
    'Date', 'Emplid_Anon', 'Hours_total',
    'Num_appts', 'Yearly_pay_total_no_summer', 'Yearly_pay_total_with_summer', 'Eff_hourly_wage_20hr',
    'Eff_hourly_wage_40hr', 'College', 'College_code', 'Department'
]

for rowIdx, rowGradGrouped in dfGradGrouped.iterrows():    
    rowDictGradGrouped = rowGradGrouped.to_dict()
    rowDictDeptSplit = {col:val for (col,val) in rowDictGradGrouped.items() if col in colsToKeep}
    
    deptsIncluded = []
    for deptIdx in range(len(rowDictGradGrouped['Department_list'])):
        college, dept = rowDictGradGrouped['College_list'][deptIdx], rowDictGradGrouped['Department_list'][deptIdx]
        
        # Ensures that each department is only added once (two appointments to the same dept shouldn't result in 2 rows)
        if dept in deptsIncluded: continue
        deptsIncluded.append(dept)
        
        # Creates a new row for each distinct department this student is being paid from
        rowDictDeptSplitCopy = rowDictDeptSplit.copy()
        rowDictDeptSplitCopy['College'] = college
        rowDictDeptSplitCopy['Department'] = dept
        deptSplitRowDicts.append(rowDictDeptSplitCopy)
        
dfDeptSplit = pd.DataFrame(data=deptSplitRowDicts)

# Utility column: Only includes the 4 letter code describing each college
dfDeptSplit['College_code'] = [row['College'][:4] for _,row in dfDeptSplit.iterrows()]


# -- Writes all derived data frames to file --
print('Writing to file...')
dfGrad.to_csv('processed_datasets/pay_data_grads_only.csv', index=False)
dfGradGrouped.to_csv('processed_datasets/pay_data_emplid_grouped.csv', index=False)
dfDeptSplit.to_csv('processed_datasets/pay_data_dept_split.csv', index=False)

print('Done!')


