var aws = require('aws-sdk');
var nodemailer = require('nodemailer');

var ses = new aws.SES();
var s3Obj = new aws.S3();
const ssmClient = new aws.SSM({region: 'us-east-1'});

const getParameter = async (parameter) => {
	return await new Promise((resolve,reject) => {
		ssmClient.getParameter( { 
            Name: parameter,
            WithDecryption: true
         }, (err, result) => {
			if (err) reject(err)
            else 
            {
                if(result.Parameter) {
                    resolve(JSON.parse(result.Parameter.Value));
                }
            }
		})
	})
  }
exports.handler = async function (event, context) {
    console.log(event);
    const bucket = event.Records[0].s3.bucket.name;
    const key = decodeURIComponent(event.Records[0].s3.object.key.replace(/\+/g, ' '));
    const parameters = await getParameter(process.env.ParameterName)
    try{    
        let resp =await sendEmail(parameters, bucket, key);
        console.log(resp);   
        return resp;
    }
    catch(err)
    {
        console.log('Error');
        console.log(err);    
        return err;   
    }

};

async function sendEmail(parameters, bucket, key)
{
    let splitValue = key.split("/");
    let folderName = splitValue.slice(0, splitValue.length - 1).join('/');
    const params = {
            Bucket: bucket,
            Key: key,
            };
	    
        let resp = await new Promise((resolve,reject) => { s3Obj.getObject(params, function(err, data) {
            if (err) {
                console.log('Error');
               console.log(JSON.stringify(err));
                // error handling
                return err;
            }
            else {
                console.log('in');
                
	
            var mailOptions = {
                from: parameters[folderName].From,
                subject: parameters[folderName].Subject,
                to: parameters[folderName].To,
                html: parameters[folderName].html,
                attachments: [
                    {
                        filename: key,
                        content: data.Body,
                        contentType: data.contentType
                    }
                ]
                };
            console.log('mailOptions', mailOptions)

                console.log('Creating SES transporter');
                // create Nodemailer SES transporter
                var transporter = nodemailer.createTransport({
                    SES: ses
                });

                // send email
                transporter.sendMail(mailOptions, function (err, info) {
                    if (err) {
                        console.log(err);
                        console.log('Error sending email');
                        return err;
                        } else {
                            console.log('Email sent successfullyy');
                            return "Send email now";
                        }
                    });
				}
        });
    });
}
