const axios = require('axios');


exports.handler = function(event, context, callback) {      

    console.log('Received event:', JSON.stringify(event, null, 2));



    // A simple request-based authorizer example to demonstrate how to use request 
    // parameters to allow or deny a request. In this example, a request is  
    // authorized if the client-supplied HeaderAuth1 header, QueryString1 
    // query parameter, and stage variable of StageVar1 all match
    // specified values of 'headerValue1', 'queryValue1', and 'stageValue1',
    // respectively.

    // Retrieve request parameters from the Lambda function input:
    var headers = event.headers;
    var queryStringParameters = event.queryStringParameters;
    var pathParameters = event.pathParameters;
    var stageVariables = event.stageVariables;
    
        
    // Parse the input for the parameter values
    var tmp = event.methodArn.split(':');
    var apiGatewayArnTmp = tmp[5].split('/');
    var awsAccountId = tmp[4];
    var region = tmp[3];
    var restApiId = apiGatewayArnTmp[0];
    var stage = apiGatewayArnTmp[1];
    var method = apiGatewayArnTmp[2];
    var resource = '/'; // root resource
    if (apiGatewayArnTmp[3]) {
        resource += apiGatewayArnTmp[3];
    }
        
    // Perform authorization to return the Allow policy for correct parameters and 
    // the 'Unauthorized' error, otherwise.
    var authResponse = {};
    var condition = {};
    condition.IpAddress = {};
    
    

    if(headers["Authorization"] != undefined){
      axios.defaults.headers.common['Authorization'] = headers["Authorization"];
    } else if(queryStringParameters['Authorization'] != undefined) {
      axios.defaults.headers.common['Authorization'] = queryStringParameters["Authorization"];
    } else if(queryStringParameters['authorization'] != undefined) {
       axios.defaults.headers.common['Authorization'] = queryStringParameters["authorization"];
    }else{
      axios.defaults.headers.common['Authorization'] = headers["authorization"];        
    }
    let  lenderid = "";
    
    if(headers["lenderid"] != undefined){
      axios.defaults.headers.common['lenderid'] = headers["lenderid"];
      lenderid = headers["lenderid"];
    } else if(queryStringParameters['lender']) {
      axios.defaults.headers.common['lender'] = queryStringParameters["lender"];
      lenderid = queryStringParameters["lender"];
    }
     else if(queryStringParameters['lenderId']) {
      axios.defaults.headers.common['lenderId'] = queryStringParameters["lenderId"];
      lenderid = queryStringParameters["lenderId"];
    }
    else if (headers["lenderId"] != undefined){
      axios.defaults.headers.common['lenderId'] = headers["lenderId"]; 
      lenderid = headers["lenderId"];
    }
    var token = lenderid+"_cyncsoftware_com";
    console.log("token",token);
    
    console.log("lender id for req", lenderid);
    
    axios.get('https://'+lenderid+'.cyncsoftware.com/api/v1/users/get_user_info.json')
      .then(function (response) {
        // console.log("response", response.data );
        try{
        callback(null, generateAllow('me', event.methodArn,token));
        }catch{
         console.log("authorized and failed in callback"); 
        }
      })
      .catch(function (error) {
        console.log("error", error);
        try{
         callback("Unauthorized");
        }catch{
         console.log("Unauthorized and failed in callback"); 
        }
      })
      .then(function () {
        // always executed
      });
    
    


    // if(headers.authorization != 'allow'){
    //     callback(null, generateAllow('me', event.methodArn,token));
    //  }  else {
    //   callback("Unauthorized");
    // }
}
     
// Help function to generate an IAM policy
var generatePolicy = function(principalId, effect, resource,token) {
    // Required output:
    var authResponse = {};
    authResponse.principalId = principalId;
    if (effect && resource) {
        var policyDocument = {};
        policyDocument.Version = '2012-10-17'; // default version
        policyDocument.Statement = [];
        var statementOne = {};
        statementOne.Action = 'execute-api:Invoke'; // default action
        statementOne.Effect = effect;
        statementOne.Resource = resource;
        policyDocument.Statement[0] = statementOne;
        authResponse.policyDocument = policyDocument;
    }
    // Optional output with custom properties of the String, Number or Boolean type.
    authResponse.context = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": true
    };
    authResponse.usageIdentifierKey = token;
    return authResponse;
}
     
var generateAllow = function(principalId, resource,token) {
    return generatePolicy(principalId, 'Allow', resource,token);
}
     
var generateDeny = function(principalId, resource) {
    return generatePolicy(principalId, 'Deny', resource);
}