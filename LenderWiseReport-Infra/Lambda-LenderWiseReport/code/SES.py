import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from configuration_file import *

sender = sender_email
recipient = recipient_email
subject = email_subject
body = email_body
bucket_name = generic_bucket_name
file_name = generic_report_file_path

def send_email_with_s3_attachment(sender, recipient, subject, body, bucket_name, file_name):
    # Create a new SES resource
    ses_client = boto3.client('ses', region_name='us-east-1')

    for recipient_address in recipient:
        # Create a multipart/mixed email message
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient_address

        # Add the email body as a MIMEText part
        msg.attach(MIMEText(body, 'plain'))

        # Get the file from S3
        s3_client = boto3.client('s3')
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
            file_content = response['Body'].read()
        except ClientError as e:
            print(f"Error getting file from S3: {e.response['Error']['Message']}")
            return

        # Add the S3 file as a MIMEApplication part
        attachment = MIMEApplication(file_content)
        attachment.add_header('Content-Disposition', 'attachment', filename=file_name)
        msg.attach(attachment)

        try:
            # Send the raw email message
            response = ses_client.send_raw_email(
                Source=sender,
                Destinations=[recipient_address],
                RawMessage={'Data': msg.as_string()}
            )
        except ClientError as e:
            # Handle any errors that occur during sending
            print(f"Error sending email: {e.response['Error']['Message']}")
        else:
            print(f"Email sent successfully to {recipient_address}!")

def main():
    # Send the email with S3 attachment
    send_email_with_s3_attachment(sender, recipient, subject, body, bucket_name, file_name)

if __name__ == '__main__':
    main()
