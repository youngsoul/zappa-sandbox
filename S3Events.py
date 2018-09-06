import boto3

def lambda_handler(event, context):
    print("Lambda Handler")
    return 'done'


def process_upload_function(event, context):

    """
    Process a file upload to S3
    :param event:
    :param context:
    :return:
    """
    print("process_upload_function")
    s3_client = boto3.client('s3')
    bucket = "none"
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Bucket: {bucket}, Key: {key}")

        # Get the bytes from S3
        s3_client.download_file(bucket, key, '/tmp/' + key)  # Download this file to writable tmp space.
        file_bytes = open('/tmp/' + key).read()
        print(file_bytes)
    except:
        pass

    return bucket
