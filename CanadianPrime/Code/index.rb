require 'json'
require 'lambda_runtime'

LambdaRuntime.configure do |config|
  config.function_name = 'hello_lambda'
end

def handler(event:, context:)
  # Process the event data
  name = event['name'] || 'World'

  # Create a response
  response = {
    statusCode: 200,
    body: "Hello, #{name}!"
  }

  response.to_json
end

LambdaRuntime.run { |event, context| handler(event: event, context: context) }
