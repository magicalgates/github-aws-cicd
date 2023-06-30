import pandas as pd
from configuration_file import *
from s3_import import *

def service():

    # Read the XLSX file into a DataFrame
    df = service_report_import()

    dataframe = pd.DataFrame(df)

    # Replace specific service names with desired names
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Elastic Compute Cloud - Compute', 'EC2-Instances($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon ElastiCache', 'ElastiCache($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS CloudTrail', 'CloudTrail($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS CodePipeline', 'CodePipeline($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Config', 'Config($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Cost Explorer', 'Cost Explorer($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Glue', 'Glue($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Key Management Service', 'Key Management Service($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Lambda', 'Lambda($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Secrets Manager', 'Secrets Manager($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Security Hub', 'Security Hub($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Step Functions', 'Step Functions($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Support (Business)', 'Support (Business)($)', regex=False)
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS Systems Manager', 'Systems Manager($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AWS X-Ray', 'X-Ray($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon API Gateway', 'API Gateway($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon CloudFront', 'CloudFront($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon DynamoDB', 'DynamoDB($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon EC2 Container Registry (ECR)', 'EC2 Container Registry (ECR)($)',regex=False)
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('EC2 - Other', 'EC2-Other($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Elastic Container Service', 'Elastic Container Service($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Elastic Load Balancing', 'EC2-ELB($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon GuardDuty', 'GuardDuty($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Inspector', 'Inspector($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Lightsail', 'Lightsail($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Relational Database Service', 'Relational Database Service($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Route 53', 'Route 53($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Simple Email Service', 'SES($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Simple Notification Service', 'SNS($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Simple Queue Service', 'SQS($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Simple Storage Service', 'S3($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Amazon Virtual Private Cloud', 'VPC($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('AmazonCloudWatch', 'CloudWatch($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Barracuda CloudGen WAF for AWS - PAYG', 'Barracuda CloudGen WAF for  - PAYG($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('CloudWatch Events', 'CloudWatch Events($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('CodeBuild', 'CodeBuild($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Tax', 'Tax($)')
    dataframe['Service Name'] = dataframe['Service Name'].str.replace('Trend Cloud One', 'Trend Micro Cloud One($)')

    # Drop the 'SERIAL No' column
    df2 = dataframe.drop('SERIAL No', axis=1)

    # Create a column mapping for renaming columns
    column_mapping = {'Service Name': 'Service', 'Bill In USD': 'Service total'}
    
    # Rename the columns using the mapping
    df2.rename(columns=column_mapping, inplace=True)

    # Calculate the total cost of services
    total_cost = df2['Service total'].sum()

    # Create a row with the total cost
    total_cost_row = pd.DataFrame({'Service': ['Total Cost'], 'Service total': [total_cost]})
    
    # Concatenate the original DataFrame with the total cost row
    df_concatenated = pd.concat([df2, total_cost_row])

    # Return the concatenated DataFrame
    return df_concatenated


def main():
    # Call the service function and print the result
    print(service())

if __name__ == '__main__':
    main()
