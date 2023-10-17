######## This Script Generates CPU and Memory Utilization of Autoscaling group in Daily and Montly Basis ###########

import boto3
import pandas as pd
from datetime import datetime, timedelta
import pytz  
import io

# Initialize an S3 client
s3 = boto3.client('s3')
# Initialize an cloudwatch client
cloudwatch = boto3.client('cloudwatch')

# Specify the Flag i.e,. "Daily" or "Montly"
flag = "Montly"

# Specify the Report name
report_name = "Spot_CPU_Montly_utilization"

# Specify s3 bucket name and key name.
s3_bucket_name = 'yashdemobucket007'
s3_key = 'utilization reports/' + f'{report_name}.xlsx'

# Autoscaling group name
autoscaling_group_name = 'Spot-ASG1'

# Specify the metric name i.e., 'CPUUtilization', 'mem_used_percent'
metric_name = 'CPUUtilization'

# Specify name space i.e., 'AWS/EC2', 'CWAgent'
name_space = 'AWS/EC2'

# Specify the start and end date
start_date = '2023-09-29'  
end_date = '2023-09-12'   

# Specify the IST time zone
ist_timezone = 'Asia/Kolkata'

# Create a timezone object for IST
ist_tz = pytz.timezone(ist_timezone)

# Function to fetch utilization 
def get_utilization(autoscaling_group_name, start_time, end_time):
    response = cloudwatch.get_metric_statistics(
        Namespace=name_space,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': autoscaling_group_name
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,  # 1 hour intervals
        Statistics=['Maximum', 'Minimum', 'Average'],
        Unit='Percent'
    )
    return response['Datapoints']

def daily():
    # Initialize an empty list to store daily data
    daily_data = []

    # start and end dates as datetime objects in IST
    start_date_datetime_ist = ist_tz.localize(datetime.strptime(start_date, '%Y-%m-%d'))
    end_date_datetime_ist = ist_tz.localize(datetime.strptime(end_date, '%Y-%m-%d'))

    current_date = start_date_datetime_ist
    while current_date <= end_date_datetime_ist:

        # Convert IST datetime objects to UTC for AWS CloudWatch
        current_month_start_utc = current_date.astimezone(pytz.utc)
        current_month_end_utc = (current_date + timedelta(days=1)).astimezone(pytz.utc)

        # # Initialize AWS clients
        # cloudwatch = boto3.client('cloudwatch')

        # Fetch utilization data for the current date to end date
        data_month = get_utilization(autoscaling_group_name, current_month_start_utc, current_month_end_utc)

        # Calculate Max, Min, and Avg for the current dates if data is available
        if data_month:
            max_month = max(data_month, key=lambda x: x['Maximum'])
            min_month = min(data_month, key=lambda x: x['Minimum'])
            avg_month = sum([point['Average'] for point in data_month]) / len(data_month)
        else:
            max_month = min_month = avg_month = {'Maximum': 0, 'Minimum': 0, 'Average': 0}

        # Define business hours (00:00 - 07:00 and 17:00 - 23:59) in IST
        business_start_time_1_ist = current_date.replace(hour=0, minute=0, second=0) 
        business_end_time_1_ist = current_date.replace(hour=7, minute=0, second=0) 
        business_start_time_2_ist = current_date.replace(hour=17, minute=0, second=0)
        business_end_time_2_ist = current_date.replace(hour=23, minute=59, second=59)

        # Convert IST business hours to UTC
        business_start_time_1_utc = business_start_time_1_ist.astimezone(pytz.utc) #2023-08-07 18:30 UTC
        business_end_time_1_utc = business_end_time_1_ist.astimezone(pytz.utc)
        business_start_time_2_utc = business_start_time_2_ist.astimezone(pytz.utc)
        business_end_time_2_utc = business_end_time_2_ist.astimezone(pytz.utc)

        # Fetch utilization data for business hours in IST
        data_business_1 = get_utilization(autoscaling_group_name, business_start_time_1_utc, business_end_time_1_utc)
        data_business_2 = get_utilization(autoscaling_group_name, business_start_time_2_utc, business_end_time_2_utc)

        # Calculate Max, Min, and Avg for business hours if data is available
        if data_business_1 or data_business_2:
            # Finds the Max hourly data from data business 1 and 2
            max_business = max(data_business_1 + data_business_2, key=lambda x: x['Maximum'])
            min_business = min(data_business_1 + data_business_2, key=lambda x: x['Minimum'])
            avg_business = sum([point['Average'] for point in data_business_1 + data_business_2]) / len(data_business_1 + data_business_2)
        else:
            max_business = min_business = avg_business = {'Maximum': 0, 'Minimum': 0, 'Average': 0}

        # Calculate Max, Min, and Avg for non-business hours in IST
        non_business_start_time_utc = business_end_time_1_utc
        non_business_end_time_utc = business_start_time_2_utc
        data_non_business = get_utilization(autoscaling_group_name, non_business_start_time_utc, non_business_end_time_utc)

        # Calculate Max, Min, and Avg for non-business hours if data is available
        if data_non_business:
            max_non_business = max(data_non_business, key=lambda x: x['Maximum'])
            min_non_business = min(data_non_business, key=lambda x: x['Minimum'])
            avg_non_business = sum([point['Average'] for point in data_non_business]) / len(data_non_business)
        else:
            max_non_business = min_non_business = avg_non_business = {'Maximum': 0, 'Minimum': 0, 'Average': 0}

        # Append the daily data to the list
        daily_data.append({
            'Date': current_date.strftime('%Y-%m-%d'),
            'Max (Month)': f'{max_month["Maximum"]:.1f}%',
            'Min (Month)': f'{min_month["Minimum"]:.1f}%',
            'Avg (Month)': f'{avg_month:.1f}%',
            'Max (Business hour)': f'{max_business["Maximum"]:.1f}%',
            'Min (Business hour)': f'{min_business["Minimum"]:.1f}%',
            'Avg (Business hour)': f'{avg_business:.1f}%',
            'Max (Non Business hour)': f'{max_non_business["Maximum"]:.1f}%',
            'Min (Non Business hour)': f'{min_non_business["Minimum"]:.1f}%',
            'Avg (Non Business hour)': f'{avg_non_business:.1f}%'
        })

        # Move to the next day
        current_date += timedelta(days=1)

    # Create a Pandas DataFrame from the daily data
    df = pd.DataFrame(daily_data)
    # print(df)

    # Create an in-memory buffer for the Excel file
    excel_buffer = io.BytesIO()

    # Export the DataFrame to the Excel buffer
    df.to_excel(excel_buffer, index=False)

    # Upload the Excel buffer to S3
    excel_buffer.seek(0)  # Reset the buffer's position to the beginning
    s3.upload_fileobj(excel_buffer, s3_bucket_name, s3_key)  # Use upload_fileobj to upload the buffer

    # Export the DataFrame to an Excel file
    # df.to_excel(f'{report_name}.xlsx', index=False)

    # print(f'{metric_name} of {autoscaling_group_name} from {start_date} to {end_date} is generated.')

def montly():
    # Initialize an empty list to store monthly data
    monthly_data = []

    # start and end dates as datetime objects in IST
    start_date_datetime_ist = ist_tz.localize(datetime.strptime(start_date, '%Y-%m-%d'))
    end_date_datetime_ist = ist_tz.localize(datetime.strptime(end_date, '%Y-%m-%d'))

    # Loop through each month in the date range
    current_month_start = start_date_datetime_ist
    while current_month_start <= end_date_datetime_ist:
        # Calculate the end date for the current month
        current_month_end = current_month_start + timedelta(days=31)
        current_month_end = min(current_month_end, end_date_datetime_ist)  

        # Convert IST datetime objects to UTC for AWS CloudWatch
        current_month_start_utc = current_month_start.astimezone(pytz.utc)
        current_month_end_utc = current_month_end.astimezone(pytz.utc)

        # Fetch utilization data for the current month
        data_month = get_utilization(autoscaling_group_name, current_month_start_utc, current_month_end_utc)

        # Calculate Max, Min, and Avg for the current month if data is available
        if data_month:
            max_month = max(data_month, key=lambda x: x['Maximum'])
            min_month = min(data_month, key=lambda x: x['Minimum'])
            avg_month = sum([point['Average'] for point in data_month]) / len(data_month)
        else:
            max_month = min_month = avg_month = {'Maximum': 0, 'Minimum': 0, 'Average': 0}

        # Define business hours (00:00 - 07:00 and 17:00 - 23:59) in IST for the current month
        business_start_time_1_ist = current_month_start.replace(hour=0, minute=0, second=0)
        business_end_time_1_ist = current_month_start.replace(hour=7, minute=0, second=0)
        business_start_time_2_ist = current_month_start.replace(hour=17, minute=0, second=0)
        business_end_time_2_ist = current_month_start.replace(hour=23, minute=59, second=59)

        # Convert IST business hours to UTC for the current month
        business_start_time_1_utc = business_start_time_1_ist.astimezone(pytz.utc)
        business_end_time_1_utc = business_end_time_1_ist.astimezone(pytz.utc)
        business_start_time_2_utc = business_start_time_2_ist.astimezone(pytz.utc)
        business_end_time_2_utc = business_end_time_2_ist.astimezone(pytz.utc)

        # Fetch utilization data for business hours in the current month
        data_business_1 = get_utilization(autoscaling_group_name, business_start_time_1_utc, business_end_time_1_utc)
        data_business_2 = get_utilization(autoscaling_group_name, business_start_time_2_utc, business_end_time_2_utc)

        # Calculate Max, Min, and Avg for business hours in the current month if data is available
        if data_business_1 or data_business_2:
            max_business = max(data_business_1 + data_business_2, key=lambda x: x['Maximum'])
            min_business = min(data_business_1 + data_business_2, key=lambda x: x['Minimum'])
            avg_business = sum([point['Average'] for point in data_business_1 + data_business_2]) / len(data_business_1 + data_business_2)
        else:
            max_business = min_business = avg_business = {'Maximum': 0, 'Minimum': 0, 'Average': 0}

        # Calculate Max, Min, and Avg for non-business hours in the current month
        data_non_business = [point for point in data_month if point['Timestamp'] < business_start_time_1_utc or point['Timestamp'] > business_end_time_2_utc]

        # Calculate Max, Min, and Avg for non-business hours in the current month if data is available
        if data_non_business:
            max_non_business = max(data_non_business, key=lambda x: x['Maximum'])
            min_non_business = min(data_non_business, key=lambda x: x['Minimum'])
            avg_non_business = sum([point['Average'] for point in data_non_business]) / len(data_non_business)
        else:
            max_non_business = min_non_business = avg_non_business = {'Maximum': 0, 'Minimum': 0, 'Average': 0}

        # Append the monthly data to the list
        monthly_data.append({
            'Month': current_month_start.strftime('%Y-%m'),
            'Max (Month)': f'{max_month["Maximum"]:.1f}%',
            'Min (Month)': f'{min_month["Minimum"]:.1f}%',
            'Avg (Month)': f'{avg_month:.1f}%',
            'Max (Business hour)': f'{max_business["Maximum"]:.1f}%',
            'Min (Business hour)': f'{min_business["Minimum"]:.1f}%',
            'Avg (Business hour)': f'{avg_business:.1f}%',
            'Max (Non Business hour)': f'{max_non_business["Maximum"]:.1f}%',
            'Min (Non Business hour)': f'{min_non_business["Minimum"]:.1f}%',
            'Avg (Non Business hour)': f'{avg_non_business:.1f}%'
        })

        # Move to the next month
        current_month_start = current_month_start.replace(day=1) + timedelta(days=32)

    # Create a Pandas DataFrame from the monthly data
    df = pd.DataFrame(monthly_data)
    # print(df)

    # Create an in-memory buffer for the Excel file
    excel_buffer = io.BytesIO()

    # Export the DataFrame to the Excel buffer
    df.to_excel(excel_buffer, index=False)

    # Upload the Excel buffer to S3
    excel_buffer.seek(0)  # Reset the buffer's position to the beginning
    s3.upload_fileobj(excel_buffer, s3_bucket_name, s3_key)  # Use upload_fileobj to upload the buffer

    # Export the DataFrame to an Excel file
    # df.to_excel(f'{report_name}.xlsx', index=False)

    # print(f"{metric_name}_{autoscaling_group_name}_{start_date}_{end_date}.xlsx")


def main():
    if flag == "Daily":
        print("Initializing the execution for daily basis")
        daily()
        print("Completed Execution")
    else:
        print("Initializing the execution for montly basis")
        montly()
        print("Completed Execution")

if __name__ == "__main__":
    main()
