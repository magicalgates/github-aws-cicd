import boto3
import pandas as pd
from io import BytesIO
from configuration_file import *

#Bucket name
bucket_name = generic_bucket_name
#DB Report Details
db_report_name = db_file_path
db_report_sheet = generic_db_report_sheet
#S3 Report Details
s3_report_name = s3_report_file_path
s3_report_sheet = generic_s3_report_sheet
#Service Cost Report Details
service_cost_file_name = service_cost_file_path
servicecostsheet = generic_servicecostsheet
#Lender Waf Report Details
lender_waf_report = Lender_waf_report_file_path
lender_waf_report_sheet = generic_lender_waf_report_sheet

# Set up the S3 client
s3 = boto3.client('s3')

def db_report_import():
    # Read the Excel file from S3 into a DataFrame
    s3_object = s3.get_object(Bucket=bucket_name, Key=db_report_name)
    excel_data = s3_object['Body'].read()
    df_1 = pd.read_excel(BytesIO(excel_data), sheet_name=db_report_sheet)
    # Display the DataFrame
    return df_1

def s3_report_import():
    # Read the Excel file from S3 into a DataFrame
    s3_object = s3.get_object(Bucket=bucket_name, Key=s3_report_name)
    excel_data = s3_object['Body'].read()
    df_2 = pd.read_excel(BytesIO(excel_data), sheet_name=s3_report_sheet)
    # Display the DataFrame
    return df_2

def service_report_import():
    # Read the Excel file from S3 into a DataFrame
    s3_object = s3.get_object(Bucket=bucket_name, Key=service_cost_file_name)
    excel_data = s3_object['Body'].read()
    df_3 = pd.read_excel(BytesIO(excel_data), sheet_name=servicecostsheet)
    # Display the DataFrame
    return df_3

def lender_report_import():
    # Read the Excel file from S3 into a DataFrame
    s3_object = s3.get_object(Bucket=bucket_name, Key=Lender_waf_report_file_path)
    excel_data = s3_object['Body'].read()
    df_4 = pd.read_excel(BytesIO(excel_data), sheet_name=generic_lender_waf_report_sheet)
    # Display the DataFrame
    return df_4

def main():
    a = db_report_import()
    b = s3_report_import()
    c = service_report_import()
    d = lender_report_import()
    # print(a)
    # print(b)
    # print(c)
    # print(d)

if __name__ == '__main__':
    main()

