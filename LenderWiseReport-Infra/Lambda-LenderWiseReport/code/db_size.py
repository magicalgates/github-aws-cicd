import pandas as pd
from configuration_file import *
from s3_import import *

def lender_names():
    lender_fn = db_report_import()
    #Read the Excel file into a DataFrame
    dataframe = pd.DataFrame(lender_fn)
    return dataframe["Lender Name"]

def db_size():
    waf_fn = db_report_import()
    #Read the Excel file into a DataFrame
    dataframe = pd.DataFrame(waf_fn)

    # Append '.cyncsoftware.com' to the 'Lender Name' column
    dataframe["Lender Name"] = dataframe["Lender Name"] + '.cyncsoftware.com'

    # Remove spaces from the 'Lender Name' column
    dataframe["Lender Name"] = dataframe["Lender Name"].str.replace(' ', '')

    # Calculate the total size in MB
    total_mb = dataframe["Size (MB)"].sum()

    # Create a DataFrame row with the total size
    total_mb_row = pd.DataFrame({'Lender Name': ['Total'], 'Size (MB)': [total_mb]})

    # Concatenate the total size row to the DataFrame
    df_concatenated = pd.concat([dataframe, total_mb_row])

    # Drop the 'Display Name' column
    df2 = df_concatenated.drop('Display Name', axis=1)

    # Calculate the DB Usage percentage and format as percentages with two decimal places
    df2['DB Usage %'] = (df2['Size (MB)'] / total_mb) * 100
    df2['DB Usage %'] = df2['DB Usage %'].map('{:.6f}%'.format)

    # Return the resulting DataFrame
    return df2

def main():
    # Call the db_size function
    a = db_size()
    print(a)

if __name__ == '__main__':
    main()
