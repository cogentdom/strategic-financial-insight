import pandas as pd
import support.supporting_funcs as funcs
import glob

def cols():
    """Return column name descriptions"""
    ipi_cols = pd.read_csv("col_only.csv",low_memory=False)
    return ipi_cols

def empl(out=False):
    """compile employment files and produuce csv"""
    empl_files = glob.glob("employment/l*xlsx")
    emp = pd.concat([pd.read_excel(f,header=[2,3,4]) for f in empl_files])
    emp.columns = emp.columns.map(' '.join).str.strip('|')
    emp = emp[emp['State FIPS Code'] == 16]
    if out:
        all_data.to_csv("emp_data.csv",index=False)
    return emp

def emp():
    """return already created employee data file"""
    data = pd.read_csv("emp_data.csv")
    return data

def gps():
    """return already created gps data file"""
    gps_data = pd.read_csv("gps_data.csv")
    return(gps_data)

def ipi_abb():
    # This function limits the years and cities to the best data we have
    print("note this requires ipi_final.csv to be created (call all_data(out=True)")
    ipi_data = pd.read_csv("ipi_final.csv",low_memory=False)
    ipi_data = ipi_data.loc[(ipi_data['Year4'] == 1997) | (ipi_data['Year4'] == 2002)|(ipi_data['Year4'] == 2012) | (ipi_data['Year4'] == 2007)]
    cities = pd.read_csv("best_cities.csv")
    ipi_data = ipi_data.merge(cities,how = 'right', on='Name')
    return(ipi_data)

def all_data(out=False,norm=True):
    # This function will merge ipi with gps and emp.
    # and adjust for inflation
    # and create new columns for rates/100k and money percents of whole
    # and get a category column for city size
    print("Loading IPI data")
    ipi_data = funcs.gen_real_dollars() # Get Inflation Adjusted Data
    print("Getting GPS")
    gps_data = gps()
    print("Getting Employees")
    emp_data = emp()
    print("Merge Everything")
    merge1 = ipi_data.merge(emp_data,left_on=['FIPS_County','Year4'],right_on=['County FIPS Code','County FIPS Year'])
    all_data = merge1.merge(gps_data,how='left',on = 'Name')
    if norm:
        print("Normalize Columns")
        all_data = funcs.normalize(all_data)
    print("Categorize City Size")
    all_data = funcs.categorize_size(all_data)
    if out:
        print("writing file to ipi_final.csv")
        all_data.to_csv("ipi_final.csv",index=False)
    return all_data

