# Fitness Souls infrastructure

AWS architecture:

DynamoDb - serverless database
Lambda Functions - make changes in the database
API Gateway - provides single and uniform entry point to work with lambda's
CloudWatch - logging

To implement:
Cognito - for user authorization and authentication
Amplify - to host frontend