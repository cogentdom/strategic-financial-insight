"""
Supporting Functions Module for Idaho Policy Institute Analysis

This module provides utility functions for data preprocessing, feature engineering,
and data exploration for the IPI financial analysis project.

Functions:
    search_all: Search DataFrame columns by pattern
    search_column: Search column descriptions by keyword
    normalize: Create normalized features (per-capita, percentages)
    categorize_size: Categorize cities by population size
    gen_real_dollars: Adjust financial data for inflation
    conv: Calculate inflation multiplier
    drop_orig: Remove original columns after normalization

Author: Dominik Huffield
Project: Strategic Financial Insight - Idaho Policy Institute
"""

import pandas as pd
import support.load_data as load
import re
import numpy as np


def search_all(data, search, silent=False):
    """
    Search DataFrame columns by pattern using case-insensitive regex.
    
    Args:
        data (pd.DataFrame): DataFrame to search within
        search (str): Search pattern (regex supported)
        silent (bool): If False, prints all matching columns. Default is False.
    
    Returns:
        numpy.ndarray: Array of column names matching the search pattern
    
    Example:
        >>> import support.load_data as load
        >>> data = load.all_data()
        >>> 
        >>> # Find all crime-related columns
        >>> crime_cols = search_all(data, 'crime')
        >>> 
        >>> # Find all revenue columns silently
        >>> revenue_cols = search_all(data, 'revenue', silent=True)
    """
    # Case-insensitive regex search
    result = data.filter(regex='(?i)' + search).columns.get_values()
    
    # Print results unless silenced
    if not silent:
        for item in result:
            print(item)
    
    return result


def search_column(searchstr, coldata, array=False, disp=False):
    """
    Search column descriptions using a keyword or pattern.
    
    Searches the 'ShortName' field in column metadata for matches,
    optionally displaying the corresponding 'LongName' descriptions.
    
    Args:
        searchstr (str): Search string or regex pattern
        coldata (pd.DataFrame): Column metadata DataFrame (from load.cols())
        array (bool): Legacy parameter, kept for compatibility. Default is False.
        disp (bool): If True, prints the long descriptions. Default is False.
    
    Returns:
        numpy.ndarray: Array of ShortName values matching the search
    
    Example:
        >>> import support.load_data as load
        >>> columns = load.cols()
        >>> 
        >>> # Search for expenditure columns and display descriptions
        >>> exp_cols = search_column('expenditure', columns, disp=True)
        >>> 
        >>> # Search for population-related columns
        >>> pop_cols = search_column('population', columns)
    """
    # Add case-insensitive flag to search string
    searchstr = "(?i)" + searchstr
    
    # Filter columns matching the search pattern
    result = coldata[coldata["ShortName"].str.contains(searchstr, regex=True) == True]
    
    # Optionally display long descriptions
    if disp:
        for item in result['LongName']:
            print(item)
    
    return result['ShortName'].get_values()

def normalize(input):
    """
    Create normalized features for better cross-city comparisons.
    
    This function generates three types of normalized features:
    1. Expenditure items as percentage of total expenditure (*_PerExp)
    2. Revenue items as percentage of total revenue (*_PerRev)
    3. Count variables as rates per 100,000 population (*_100k)
    
    Args:
        input (pd.DataFrame): Raw data with financial and demographic variables
    
    Returns:
        pd.DataFrame: Input DataFrame with additional normalized columns
    
    Normalized Features Created:
        - *_PerExp: What percentage of total spending goes to this category
        - *_PerRev: What percentage of total revenue comes from this source
        - *_100k: Rate per 100,000 population (for crime, employment, etc.)
    
    Note:
        - Replaces zeros with NaN to avoid division errors
        - Population zeros are replaced with NaN and interpolated
        - Original columns are retained alongside normalized versions
    
    Example:
        >>> data = load.all_data(norm=False)  # Load without normalization
        >>> normalized_data = normalize(data)
        >>> 
        >>> # Compare police expenditure across cities of different sizes
        >>> print(normalized_data[['Name', 'Police_PerExp', 'size']])
    """
    # Load column metadata
    cols = pd.read_csv('col_only.csv')
    
    # Define column ranges for different types of financial data
    exp_cols = cols['ShortName'].iloc[np.concatenate([np.arange(145, 593)])].to_list()
    rev_cols = cols['ShortName'].iloc[np.concatenate([np.arange(19, 143)])].to_list()
    rate_cols = cols['ShortName'].iloc[
        np.concatenate([np.arange(594, 610), np.arange(612, 614), [144, 18]])
    ].to_list()

    # Normalize expenditure columns as percentage of total expenditure
    input['Total_Expenditure'] = input['Total_Expenditure'].replace(0, np.nan)
    for item in exp_cols:
        input[item + "_PerExp"] = (input[item] / input['Total_Expenditure']) * 100

    # Normalize revenue columns as percentage of total revenue
    input['Total_Revenue'] = input['Total_Revenue'].replace(0, np.nan)
    for item in rev_cols:
        input[item + "_PerRev"] = (input[item] / input['Total_Revenue']) * 100

    # Normalize rate columns (crime, employment, etc.) per 100k population
    input['Population'] = input['Population'].replace(0, np.nan).interpolate()
    for item in rate_cols:
        input[item + "_100k"] = (input[item] / input['Population']) * 100000
    
    return input

def categorize_size(input):
    """
    Categorize cities by population size into rural, non-urban, and urban.
    
    Uses Census Bureau definitions for community classification:
    - Rural: Population < 2,500
    - Non-urban: 2,500 <= Population < 50,000
    - Urban: Population >= 50,000
    
    Args:
        input (pd.DataFrame): DataFrame with 'Population' column
    
    Returns:
        pd.DataFrame: Input DataFrame with added 'size' column
    
    Categories:
        - 'rural': Small communities and towns (< 2,500)
        - 'non-urban': Mid-sized towns and small cities (2,500 - 49,999)
        - 'urban': Large cities (>= 50,000)
        - NaN: Invalid or missing population data
    
    Example:
        >>> data = load.all_data(norm=False)
        >>> data = categorize_size(data)
        >>> 
        >>> # Compare crime rates by city size
        >>> print(data.groupby('size')['Total_Crime_100k'].mean())
    """
    # Initialize size column
    input['size'] = 'na'
    
    def category(data):
        """Helper function to assign category to each row."""
        pop = data['Population']
        
        if pop < 2500:
            data['size'] = 'rural'
        elif 2500 <= pop < 50000:
            data['size'] = 'non-urban'
        elif pop >= 50000:
            data['size'] = 'urban'
        else:
            # Handle missing or invalid population values
            data['size'] = np.nan
        
        return data
    
    return input.apply(category, axis=1)


def conv(init_val):
    """
    Calculate inflation multiplier to convert to October 2019 dollars.
    
    Uses CPI baseline of 257.346 (October 2019) to calculate the multiplier
    needed to adjust historical dollar amounts for inflation.
    
    Args:
        init_val (float): Historical CPI value
    
    Returns:
        float: Inflation multiplier (multiply historical $ by this value)
    
    Formula:
        multiplier = 1 + ((CPI_2019 - CPI_historical) / CPI_historical)
    
    Example:
        >>> # If CPI in 2000 was 172.2
        >>> multiplier = conv(172.2)
        >>> # $100 in 2000 = $100 * multiplier in 2019 dollars
    """
    CPI_OCT_2019 = 257.346
    return 1 + ((CPI_OCT_2019 - init_val) / init_val)


def gen_real_dollars(out=False):
    """
    Adjust all financial data for inflation to October 2019 dollars.
    
    This function:
    1. Loads CPI (Consumer Price Index) data from BLS
    2. Calculates inflation multipliers for each year
    3. Adjusts all financial columns (revenue, expenditure, debt, etc.)
    4. Returns inflation-adjusted dataset
    
    Args:
        out (bool): If True, saves adjusted data to 'ipi_real2019.csv'. Default is False.
    
    Returns:
        pd.DataFrame: Complete IPI dataset with all financial values in Oct 2019 dollars
    
    Adjustment Method:
        - Uses BLS Consumer Price Index (CPI-U) data
        - Baseline: October 2019 (CPI = 257.346)
        - All financial data multiplied by appropriate inflation factor
    
    Note:
        This function is called automatically by load.all_data(), so typically
        you don't need to call it directly.
    
    Example:
        >>> # Get inflation-adjusted financial data
        >>> real_data = gen_real_dollars(out=True)
        >>> 
        >>> # All dollar amounts are now comparable across years
        >>> print(real_data[['Name', 'Year4', 'Total_Expenditure']])
    """
    # Load CPI inflation statistics from Bureau of Labor Statistics
    cpi_df = pd.read_excel('bls_cpi_stats.xlsx', header=11)
    cpi_df = cpi_df.loc[:, ['Year', 'Annual']]
    
    # Calculate inflation multiplier for each year
    cpi_df['Inflation'] = cpi_df['Annual'].map(conv)

    # Load column metadata and identify financial columns
    names = pd.read_csv('col_only.csv')
    field_names = names['ShortName'].iloc[
        np.concatenate([np.array([0, 2]), np.arange(18, 594), [616]])
    ]

    # Load complete municipal database
    data_all = pd.read_excel('Idaho_Municipal_Database_03052019.xlsx', header=1)
    finan_df = data_all.loc[:, field_names]
    
    print("Adjusting for Inflation")
    
    # Merge financial data with inflation multipliers
    tmp_df = pd.merge(finan_df, cpi_df, left_on='Year4', right_on='Year', how='left')
    tmp_df.drop(columns=['Name', 'Year4', 'Year', 'Annual'], inplace=True)
    
    # Apply inflation adjustment to all financial columns
    finan_fields = tmp_df.drop(columns=['Inflation']).columns
    tmp_df = tmp_df[finan_fields].multiply(tmp_df['Inflation'], axis='index')
    
    # Reconstruct complete dataset with adjusted financial columns
    real_df = data_all.drop(columns=finan_fields)
    real_df = pd.concat([real_df, tmp_df], axis=1)
    real_df = real_df[names['ShortName']]
    
    # Optionally save to CSV
    if out:
        real_df.to_csv('ipi_real2019.csv', index=False)
    
    return real_df

def drop_orig(data):
    """
    Remove original columns after normalization, keeping only normalized features.
    
    After calling normalize(), you may want to remove the raw columns to:
    - Reduce dataset size
    - Focus analysis on normalized features only
    - Avoid accidentally using non-comparable raw values
    
    Args:
        data (pd.DataFrame): Normalized DataFrame (output of normalize())
    
    Returns:
        pd.DataFrame: DataFrame with original expenditure, revenue, and rate columns removed
    
    Columns Removed:
        - Original expenditure columns (keeps *_PerExp versions)
        - Original revenue columns (keeps *_PerRev versions)
        - Original rate columns (keeps *_100k versions)
    
    Warning:
        This operation modifies the DataFrame in-place. Make a copy first if you
        want to keep the original columns.
    
    Example:
        >>> data = load.all_data(norm=True)
        >>> 
        >>> # Keep both original and normalized columns
        >>> data_full = data.copy()
        >>> 
        >>> # Drop original columns for cleaner analysis
        >>> data_normalized_only = drop_orig(data)
        >>> 
        >>> # Now only *_PerExp, *_PerRev, and *_100k columns remain
    """
    # Load column metadata
    cols = pd.read_csv('col_only.csv')
    
    # Identify expenditure columns to drop
    to_drop = cols['ShortName'].iloc[np.concatenate([np.arange(145, 593)])].to_list()
    
    # Add revenue columns
    to_drop = to_drop + cols['ShortName'].iloc[np.concatenate([np.arange(19, 143)])].to_list()
    
    # Add rate columns (crime, employment, etc.)
    to_drop = to_drop + cols['ShortName'].iloc[
        np.concatenate([np.arange(594, 610), np.arange(612, 614), [144, 18]])
    ].to_list()
    
    # Drop columns in-place
    data.drop(columns=to_drop, inplace=True)
    
    return data