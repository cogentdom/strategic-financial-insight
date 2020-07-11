import pandas as pd
import support.load_data as load
import re
import numpy as np

def search_all(data,search,silent=False):
    result = (data.filter(regex='(?i)'+search).columns.get_values())
    if not silent:
        for item in result:
            print(item)
    return result
def search_column(searchstr,coldata,array=False,disp=False):
    ## allows us to search for column descriptions using a search string
    searchstr = "(?i)" + searchstr
    if not array:
        result= coldata[coldata["ShortName"].str.contains(searchstr, regex=True) == True]
    else:
        result =  coldata[coldata["ShortName"].str.contains(searchstr, regex=True) == True]
    if disp:
        for item in result['LongName']:
            print(item)
    return result['ShortName'].get_values()

def normalize(input):
    # normalize stuff and create new variables
    cols = pd.read_csv('col_only.csv')
    exp_cols = cols['ShortName'].iloc[ np.concatenate([np.arange(145,593)])].to_list()
    rev_cols = cols['ShortName'].iloc[ np.concatenate([np.arange(19,143)])].to_list()
    rate_cols = cols['ShortName'].iloc[ np.concatenate([np.arange(594,610),np.arange(612,614),[144,18]])].to_list()

    input['Total_Expenditure'] = input['Total_Expenditure'].replace(0, np.nan)
    for item in exp_cols:
        input[item + "_PerExp"] = (input[item] / input['Total_Expenditure']) * 100

    input['Total_Revenue'] = input['Total_Revenue'].replace(0, np.nan)
    for item in rev_cols:
        input[item + "_PerRev"] = (input[item] / input['Total_Revenue']) * 100

    input['Population'] = input['Population'].replace(0, np.nan).interpolate()
    for item in rate_cols:
        input[item + "_100k"] = (input[item] / input['Population']) * 100000
    return input

def categorize_size(input):
    """do nothing"""

    # lower = int(input['Population'].quantile(0.33)//1)
    # upper = int(input['Population'].quantile(0.66)//1)

    input['size'] = 'na'
    def category(data):
        if data['Population'] < 50000 and (data['Population'] > 2500 ):
            data['size'] = 'non-urban'
        elif data['Population'] > 50000:
            data['size'] = 'urban'
        elif data['Population'] < 2500:
            data['size'] = 'rural'
        else:
            data['size'] = np.nan
        return data
    return input.apply(category,axis=1)


def conv(init_val):
    return (1+((257.346 - init_val)/init_val))

def gen_real_dollars(out=False):

    # Get CPI Inflation Stats
    cpi_df = pd.read_excel('bls_cpi_stats.xlsx', header=11)
    cpi_df = cpi_df.loc[:,['Year','Annual']]
    cpi_df['Inflation'] = cpi_df['Annual'].map(conv)

    # Get IPI Columns
    names = pd.read_csv('col_only.csv')
    field_names = names['ShortName'].iloc[np.concatenate([np.array([0,2]),np.arange(18,594), [616]])]

    # Get Municipal Data
    data_all = pd.read_excel('Idaho_Municipal_Database_03052019.xlsx', header=1)
    finan_df = data_all.loc[:,field_names]
    print("Adjusting for Inflation")
    tmp_df = pd.merge(finan_df, cpi_df, left_on='Year4', right_on='Year', how='left')
    tmp_df.drop(columns=['Name', 'Year4', 'Year', 'Annual'], inplace=True)
    finan_fields = tmp_df.drop(columns=['Inflation']).columns
    tmp_df = tmp_df[finan_fields].multiply(tmp_df['Inflation'], axis='index')
    real_df = data_all.drop(columns=finan_fields)
    real_df = pd.concat([real_df,tmp_df],axis=1)
    real_df = real_df[names['ShortName']]
    if out:
        real_df.to_csv('ipi_real2019.csv', index=False)
    return real_df

def drop_orig(data):
    """If you want to drop the original columns after normalizing"""
    cols = pd.read_csv('col_only.csv')
    to_drop = cols['ShortName'].iloc[np.concatenate([np.arange(145, 593)])].to_list()
    to_drop = to_drop + cols['ShortName'].iloc[np.concatenate([np.arange(19, 143)])].to_list()
    to_drop = to_drop + cols['ShortName'].iloc[np.concatenate([np.arange(594, 610), np.arange(612, 614), [144, 18]])].to_list()
    data.drop(columns=to_drop,inplace=True)
    return data