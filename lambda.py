"""
Lambda Function 1: serializeImageData

A lambda function that copies an object from S3, base64 encodes it, and 
then return it (serialized data) to the step function as `image_data` in an event.
"""

import json
import boto3
import base64

s3= boto3.client('s3')

def lambda_handler(event, context):

    key = event['s3_key']
    bucket = event['s3_bucket']

    local_path = '/tmp/image.png'
    s3.download_file(bucket, key, local_path)

    with open(local_path, 'rb') as f:
        image_data = base64.b64encode(f.read())
        
    print("Event:", event.keys())
        
    # TODO implement
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

"""
Lambda Function 2: iumage-classification


A lambda function that is responsible for the classification part. It takes the image output from the 
lambda 1 function, decodes it, and then pass inferences back to the the Step Function
"""

import json
import boto3 
import base64
#from sagemaker.serializers import IdentitySerializer

runtime = boto3.client('sagemaker-runtime')
ENDPOINT = 'image-classification-2025-04-02-10-00-06-371'

def lambda_handler(event, context):

    image = base64.b64decode(event['body']['image_data']) 
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='image/png', Body=image)
    
    inferences = response['Body'].read().decode('utf-8')

    event["inferences"] = inferences
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }



"""
Lambda Function 3: Filter-Low-Confidence-Inferences

A lambda function that takes the inferences from the Lambda 2 function output and filters low-confidence inferences
(above a certain threshold indicating success)
"""

import json

THRESHOLD = .60

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        inferences_str = body.get("inferences")
        if not inferences_str:
            raise KeyError("Inferences string not found in event body")
        inferences = json.loads(inferences_str)
        max_confidence = max(inferences) >= THRESHOLD
        response_body = {
            "threshold_met": max_confidence,
            "max_confidence": max(inferences),
            "threshold": THRESHOLD,
            "raw_inferences": inferences
        }
        print("Type of response_body:", type(response_body))
        print("Value of response_body:", response_body)
        return {
            'statusCode': 200,
            'body': json.dumps(response_body)
        }
    except KeyError as e:
        print(f"Error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({"error": str(e)})
        }
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Could not decode JSON", "details": str(e)})
        }
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }
