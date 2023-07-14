#main.py parameter details(Common Generic Report)
generic_report_name = 'NDS_Systems_Generic_LenderWiseCost_Report.xlsx'
generic_Service_cost_sheet = 'NDS_Systems' 
generic_Lender_waf_sheet = 'Lender' 
generic_DB_sheet = 'DB Usage' 
generic_s3_sheet = 's3 Usage'
generic_LenderNames_sheet = 'LenderNames'

#Servicecost.py parameter details
# generic_service_cost_file_name = '436415935402_NDS_Systems.xlsx'
generic_servicecostsheet = '436415935402_NDS_Systems'

#S3_size.py parameter details
# generic_s3_report_name = 's3 bucket storage count.xlsx'
generic_s3_report_sheet = 's3 bucket storage count'

#db_size.py parameter details
# generic_db_report_name = 'DB_Report.xlsx'
generic_db_report_sheet = 'Production Lender'

#Lender_waf_request.py parameter details
# generic_lender_waf_report = 'waf-report.xlsx'
generic_lender_waf_report_sheet = 'Report'

#SES.py details
sender_email = 'yashwanth.s@idexcel.com'                                    # Specify sender email address
recipient_email = ['yashwanth.s@idexcel.com']                               # List of recipient email addresses
email_subject = 'LenderWiseCostReport'                                      # Specify email subject
email_body = 'Please find the attached report.'                             # Specify email body
email_attachment_path = 'NDS_Systems_Generic_LenderWiseCost_Report.xlsx'    # Specify the path of local report file

#s3_import.py paramater details
#Input values
# Year = 2023
Month = 'June'
s3_folder_prefix='Bills'

generic_bucket_name = 'yashdemobucket007'
db_file_path = s3_folder_prefix + '/' + Month + '/' + 'DB_Report.xlsx'
s3_report_file_path = s3_folder_prefix + '/' + Month + '/' + 's3 bucket storage count.xlsx'
service_cost_file_path = s3_folder_prefix + '/' + Month + '/' + '436415935402_NDS_Systems.xlsx'
Lender_waf_report_file_path = s3_folder_prefix + '/' + Month + '/' + 'waf-report.xlsx'
generic_report_file_path = s3_folder_prefix + '/' + Month + '/' + 'NDS_Systems_Generic_LenderWiseCost_Report.xlsx'
