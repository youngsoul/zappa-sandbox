import json
import boto3
import requests
from io import StringIO
import random
import string

"""
Lambda Role that allows for S3 access
pryan-s3-requests-test-s3-requests-env-ZappaLambdaExecutionRole

"""
print('Loading RequestsLambda function')

s3 = boto3.client('s3')


def upload_file_contents(file_contents, bucket, path, file_name):
    buf = StringIO()
    buf.write(file_contents)

    s3.put_object(Bucket=bucket, Key=f"{path}/{file_name}", Body=file_contents)


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    try:
        response = requests.get('https://api.github.com')
        print(f"*** Github response: {response.json()}")

        path = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

        upload_file_contents(json.dumps(response.json()), 'pryan-spr-test', f'dir_{path}', f'file_{path}' )

        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }

    except Exception as e:
        print(e)
        raise e
