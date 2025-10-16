"""
Data Loading Module for Idaho Policy Institute Analysis

This module provides functions to load, merge, and prepare data from multiple sources
including IPI financial data, BLS employment statistics, and geographic coordinates.

Functions:
    cols: Load column descriptions and metadata
    empl: Compile employment files from raw Excel sources
    emp: Load pre-processed employment data
    gps: Load geographic coordinates data
    ipi_abb: Load abbreviated dataset with best data quality
    all_data: Load and merge all data sources with full preprocessing

Author: Dominik Huffield
Project: Strategic Financial Insight - Idaho Policy Institute
"""

import pandas as pd
import support.supporting_funcs as funcs
import glob


def cols():
    """
    Load column name descriptions and metadata.
    
    Returns:
        pd.DataFrame: DataFrame containing ShortName and LongName descriptions
                     for all columns in the IPI dataset
    
    Example:
        >>> column_info = cols()
        >>> print(column_info[['ShortName', 'LongName']])
    """
    ipi_cols = pd.read_csv("col_only.csv", low_memory=False)
    return ipi_cols


def empl(out=False):
    """
    Compile employment files from Bureau of Labor Statistics Excel files.
    
    This function reads multiple yearly employment Excel files from the employment/
    directory, concatenates them, and filters for Idaho (FIPS code 16).
    
    Args:
        out (bool): If True, saves the compiled data to 'emp_data.csv'. Default is False.
    
    Returns:
        pd.DataFrame: Compiled employment data for Idaho counties across multiple years
    
    Note:
        - Expects Excel files matching pattern 'employment/l*xlsx'
        - Files should have 3-level headers (rows 2, 3, 4)
        - Filters for Idaho using State FIPS Code = 16
    
    Example:
        >>> emp_data = empl(out=True)  # Compile and save to CSV
    """
    # Find all employment Excel files
    empl_files = glob.glob("employment/l*xlsx")
    
    # Read and concatenate all files with multi-level headers
    emp = pd.concat([pd.read_excel(f, header=[2, 3, 4]) for f in empl_files])
    
    # Clean column names by joining multi-level headers and stripping pipes
    emp.columns = emp.columns.map(' '.join).str.strip('|')
    
    # Filter for Idaho only (FIPS code 16)
    emp = emp[emp['State FIPS Code'] == 16]
    
    # Optionally save to CSV
    if out:
        emp.to_csv("emp_data.csv", index=False)
    
    return emp


def emp():
    """
    Load pre-processed employment data from CSV.
    
    Returns:
        pd.DataFrame: Employment statistics for Idaho counties
    
    Note:
        Requires 'emp_data.csv' to exist. Generate it first using empl(out=True)
    
    Example:
        >>> employment_data = emp()
    """
    data = pd.read_csv("emp_data.csv")
    return data


def gps():
    """
    Load geographic coordinate data for Idaho cities.
    
    Returns:
        pd.DataFrame: Geographic coordinates (latitude, longitude) indexed by city name
    
    Note:
        Data sourced from GeoNames postal code database
    
    Example:
        >>> gps_coords = gps()
        >>> print(gps_coords[['Name', 'latitude', 'longitude']])
    """
    gps_data = pd.read_csv("gps_data.csv")
    return gps_data


def ipi_abb():
    """
    Load abbreviated IPI dataset with highest quality data.
    
    This function loads a subset of the full IPI data, filtering for:
    - Years with complete data: 1997, 2002, 2007, 2012
    - Top 59 cities with most complete records
    
    Returns:
        pd.DataFrame: Abbreviated dataset with best data quality
    
    Raises:
        FileNotFoundError: If ipi_final.csv doesn't exist
    
    Note:
        Requires ipi_final.csv to be created first by calling all_data(out=True)
    
    Example:
        >>> # First create the complete dataset
        >>> all_data(out=True)
        >>> 
        >>> # Then load the abbreviated version
        >>> clean_data = ipi_abb()
    """
    print("Note: This requires ipi_final.csv to be created (call all_data(out=True) first)")
    
    # Load full IPI dataset
    ipi_data = pd.read_csv("ipi_final.csv", low_memory=False)
    
    # Filter for years with complete data (every 5 years pattern)
    ipi_data = ipi_data.loc[
        (ipi_data['Year4'] == 1997) | 
        (ipi_data['Year4'] == 2002) |
        (ipi_data['Year4'] == 2007) | 
        (ipi_data['Year4'] == 2012)
    ]
    
    # Load list of cities with best data quality
    cities = pd.read_csv("best_cities.csv")
    
    # Filter for only the best cities
    ipi_data = ipi_data.merge(cities, how='right', on='Name')
    
    return ipi_data


def all_data(out=False, norm=True):
    """
    Load and merge all data sources with complete preprocessing pipeline.
    
    This is the primary function for loading a complete, analysis-ready dataset.
    It performs the following operations:
    1. Loads IPI financial data and adjusts for inflation to October 2019 dollars
    2. Loads and merges employment statistics from BLS
    3. Loads and merges geographic coordinates
    4. Creates normalized features (per-capita rates, percentages)
    5. Categorizes cities by population size
    
    Args:
        out (bool): If True, saves the complete dataset to 'ipi_final.csv'. Default is False.
        norm (bool): If True, creates normalized features (recommended). Default is True.
    
    Returns:
        pd.DataFrame: Complete merged dataset with all preprocessing applied
    
    Features Added by Normalization:
        - *_PerExp: Expenditure items as percentage of total expenditure
        - *_PerRev: Revenue items as percentage of total revenue
        - *_100k: Rates per 100,000 population
    
    City Size Categories:
        - 'rural': Population < 2,500
        - 'non-urban': 2,500 <= Population < 50,000
        - 'urban': Population >= 50,000
    
    Example:
        >>> # Load complete dataset for analysis
        >>> data = all_data(out=True, norm=True)
        >>> 
        >>> # View normalized crime rate per 100k population
        >>> print(data[['Name', 'Year4', 'Total_Crime_100k']])
    
    Note:
        This function may take several minutes to run on first execution
        due to inflation adjustments and multiple data merges.
    """
    print("Loading IPI data")
    # Load financial data with inflation adjustment to 2019 dollars
    ipi_data = funcs.gen_real_dollars()
    
    print("Getting GPS coordinates")
    gps_data = gps()
    
    print("Getting employment data")
    emp_data = emp()
    
    print("Merging IPI with employment data")
    # First merge: IPI + Employment (on county FIPS and year)
    merge1 = ipi_data.merge(
        emp_data,
        left_on=['FIPS_County', 'Year4'],
        right_on=['County FIPS Code', 'County FIPS Year']
    )
    
    print("Merging with GPS data")
    # Second merge: Add geographic coordinates (on city name)
    all_data = merge1.merge(gps_data, how='left', on='Name')
    
    # Create normalized features if requested
    if norm:
        print("Creating normalized features (per-capita, percentages)")
        all_data = funcs.normalize(all_data)
    
    print("Categorizing city sizes")
    # Add city size category based on population
    all_data = funcs.categorize_size(all_data)
    
    # Optionally save to CSV
    if out:
        print("Writing complete dataset to ipi_final.csv")
        all_data.to_csv("ipi_final.csv", index=False)
    
    return all_data

