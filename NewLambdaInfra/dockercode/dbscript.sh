#!/bin/bash

# Add your backup dir location, password, mysql location and mysqldump location
host="dev-cync-aurora-cluster.cluster-cuhlfdkunvvz.us-east-1.rds.amazonaws.com"
user="root"
ssl_ca="rds-combined-ca-bundle.pem"
pass='Idexcel123'
bucket="idxmstestbucket1"
#"cync-dev-test"
# Downloading the uploaded file from s3 bucket
echo $bucket

key=`aws s3 ls s3://${bucket} --recursive | sort | tail -n 1 | awk '{print $4}'`
echo $key
# Extracting the lender name period and file name from the json object
IFS="/" read lender_name period file_name <<< $key
work_dir="$PWD"
db="bbc"${lender_name}

# Creating the lender's wise directory
mkdir -p /tmp/${lender_name}/${period}

cd /tmp/${lender_name}/${period}

# Downloading the file from s3 bucket
aws s3 cp s3://$bucket/$key ./temp_tb.csv

curr_dir="$PWD"

_session_id=$(uuidgen)
session_id=\"${_session_id}\"
_session_id="'"$_session_id"'"

sed -e "s/$/,${session_id}/" temp_tb.csv > temp_tb_latest.csv && mv temp_tb_latest.csv temp_tb.csv
_header_columns_string="cname,cvalue,session_id"

# Importing the data from csv file to database temporary table

mysqlimport --local --fields-enclosed-by='"' --fields-terminated-by=',' --lines-terminated-by="\n" --columns=$_header_columns_string -h ${host} -u ${user} -p${pass} --ssl-ca=$work_dir/${ssl_ca} ${db} $curr_dir/temp_tb.csv

period_value=`mysql -h ${host} -u ${user} -p${pass} --ssl-ca=$work_dir/${ssl_ca} ${db} -se "SELECT str_to_date(cvalue,'%m/%d/%Y') cvalue FROM temp_tb WHERE session_id=${_session_id} LIMIT1,1;" | grep -Ev "(cvalue)"`

if [ "$period" != "$period_value" ]
then
mysql -h ${host} -u ${user} -p${pass} --ssl-ca=$work_dir/${ssl_ca} ${db} <<EOF

INSERT INTO log_tb(session_id,item,comments) values ('${_session_id}','${period_value}','Period value in the csv file doesn\'t match with uploaded file folder.');

EOF
else
mysql -h ${host} -u ${user} -p${pass} --ssl-ca=$work_dir/${ssl_ca} ${db} <<EOF

CALL ${db}.smbc_bbc_data_migrate_proc(${_session_id});

EOF
fi

rm -rf $curr_dir/temp_tb.csv