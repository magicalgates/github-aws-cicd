import pandas as pd
from configuration_file import *
from s3_import import *

def lender_request():
    
    # Read the Excel file into a DataFrame
    df = lender_report_import()
    dataframe = pd.DataFrame(df)

    # Get the column indices to delete (excluding first and last columns)
    columns_to_delete = dataframe.columns[3:-1]

    # Drop the middle columns from the DataFrame
    result_dataframe = dataframe.drop(columns=columns_to_delete)

    # Define the specific values to filter
    specific_values = ["Get's sum of bytes sent", "Post's sum of bytes sent", "other's sum of bytes sent", "Get's sum of bytes Received", "Post's sum of bytes Received", "Other's sum of bytes Received"]

    # Filter the column data based on the specific values
    filtered_df = result_dataframe[result_dataframe['metric items'].isin(specific_values)]

    # Get the name of the last column
    last_column_name = filtered_df.columns[-1]

    # Group the filtered DataFrame by 'Lender Name' and calculate the sum of the last column
    group = filtered_df.groupby('Lender Name')[last_column_name].sum().reset_index()

    # Append '.cyncsoftware.com' to the 'Lender Name' column
    group["Lender Name"] = group["Lender Name"] + '.cyncsoftware.com'

    # Compute the total sum of values for the last column
    total_request = group[last_column_name].sum()

    # Calculate the percentage allocation for each lender and add a new column
    group['Lender Allocation % (Based on WAF bytes usage report)'] = (group[last_column_name] / total_request) * 100
    group['Lender Allocation % (Based on WAF bytes usage report)'] = group['Lender Allocation % (Based on WAF bytes usage report)'].map('{:.6f}%'.format)

    # Sort the DataFrame by the 'Lender Allocation' column in descending order
    df_group_sorted = group.sort_values(by='Lender Allocation % (Based on WAF bytes usage report)', ascending=False)

    # Drop the last column from the sorted DataFrame
    df_group_sorted = df_group_sorted.drop(last_column_name, axis=1)

    # Reset the index of the sorted DataFrame
    df_group_sorted = df_group_sorted.reset_index(drop=True)

    # Return the sorted DataFrame
    return df_group_sorted

def main():
    # Call the lender_request function
    result_df = lender_request()
    print(result_df)

if __name__ == '__main__':
    main()
