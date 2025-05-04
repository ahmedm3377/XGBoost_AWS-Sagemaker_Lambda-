import boto3
import json
import ast  # needed if you're using ast.literal_eval

def lambda_handler(event, context):
    runtime_client = boto3.client('runtime.sagemaker')
    endpoint_name = 'xgboost-2025-05-02-22-34-25-239'

    try:
        # Parse JSON string from API Gateway
        body = json.loads(event['body'])

        # Safely extract and format input
        sample_data = "{},{},{},{}".format(
            ast.literal_eval(body['p1']),
            ast.literal_eval(body['p2']),
            ast.literal_eval(body['p3']),
            ast.literal_eval(body['p4'])
        )

        # Invoke SageMaker endpoint
        response = runtime_client.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='text/csv',
            Body=sample_data
        )

        # Read and format result
        result = int(float(response['Body'].read().decode('utf-8')))

        return {
            'statusCode': 200,
            'body': json.dumps({'Class': result})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }