import pandas as pd
from db_size import *
import re
from configuration_file import *
from s3_import import *

def s3_size():

    # Define the desired values to filter on
    desired_values = []

    # calling the DB function in order to get list of Lenders
    Lenders = lender_names()
    desired_values.extend(Lenders)

    # Remove spaces from each string in the list
    desired_values = [lender.strip() for lender in desired_values]
    # print(desired_values)

    # Read the Excel file into a DataFrame
    df = s3_report_import()
    dataframe = pd.DataFrame(df)

    columns_to_keep = ['Lenders', 'Storage Size in bytes']
    dataframe = dataframe.drop(dataframe.columns.difference(columns_to_keep), axis=1)

    # Filter the data based on the desired values using regex pattern matching
    # re.escape() function is used to escape special characters in the desired values before constructing the regex pattern for filtering the data
    filtered_data = dataframe[dataframe["Lenders"].str.contains('|'.join(map(re.escape, desired_values)), case=False)].copy()

    if filtered_data.empty:
        # Handle the case when desired_values are not found
        pass
    else:
        # Extract only the desired value from the 'Lenders' column using regex
        filtered_data.loc[:, 'Lenders'] = filtered_data['Lenders'].str.extract('(' + '|'.join(desired_values) + ')', expand=False)

        # Group the data by 'Lenders' and calculate the sum of 'Storage Size in bytes'
        grouped_data = filtered_data.groupby('Lenders')['Storage Size in bytes'].sum().reset_index()

        # Append '.cyncsoftware.com' to the 'Lenders' column
        grouped_data["Lenders"] = grouped_data["Lenders"] + '.cyncsoftware.com'

        # Remove spaces from the 'Lenders' column
        grouped_data["Lenders"] = grouped_data["Lenders"].str.replace(' ', '')

        # Conversion from bytes to GB and creates new column
        grouped_data['Size in GB'] = grouped_data['Storage Size in bytes'] / (1024 * 1024 * 1024)

        # Calculate the total sum of 'Storage Size in bytes'
        total_size = grouped_data['Storage Size in bytes'].sum()

        # Calculate the percentage of each lender and add a new column
        grouped_data['S3 Usage %'] = grouped_data['Storage Size in bytes'] / total_size * 100

        # Format the 'S3 Usage %' column as percentages with two decimal places
        grouped_data['S3 Usage %'] = grouped_data['S3 Usage %'].map('{:.6f}%'.format)

        # Remove the 'Storage Size in bytes' column
        grouped_data = grouped_data.drop('Storage Size in bytes', axis=1)

        # Add a total row at the end of the DataFrame
        total_row = pd.DataFrame({'Lenders': ['Total'], 'Size in GB': [total_size / (1024 * 1024 * 1024)], 'S3 Usage %': '100%'}, index=[len(grouped_data)])
        grouped_data = pd.concat([grouped_data, total_row])

        # Return the resulting DataFrame
        return grouped_data


def main():
    # Call the s3_size function with the specified file and sheet names
    a = s3_size()
    print(a)

if __name__ == '__main__':
    main()
