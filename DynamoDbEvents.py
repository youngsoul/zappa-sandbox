import json
from random import randint, choice
import boto3
import string
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb')

def dynamo_events(event, context):
    """
    "Received event": {
"Records": [
{
"eventID": "6e318f12943932a05a17dbdd09941344",
"eventName": "INSERT",
"eventVersion": "1.1",
"eventSource": "aws:dynamodb",
"awsRegion": "us-east-1",
"dynamodb": {
"ApproximateCreationDateTime": 1536550860.0,
"Keys": {
"id": {
"S": "zUxuZp3fSNsrteenR0hAB8T6ePmyZHCJ"
}
},
"NewImage": {
"payload": {
"S": "Xxc6n9aW This is the payload"
},
"id": {
"S": "zUxuZp3fSNsrteenR0hAB8T6ePmyZHCJ"
}
},
"SequenceNumber": "2100000000028176236669",
"SizeBytes": 103,
"StreamViewType": "NEW_AND_OLD_IMAGES"
},
"eventSourceARN": "arn:aws:dynamodb:us-east-1:485071734737:table/zappa_stream_table/stream/2018-09-10T03:11:38.835"
},
    :param event:
    :param context:
    :return:
    """
    logger.debug("Received event: " + json.dumps(event, indent=2))
    for record in event['Records']:
        logger.debug(f"eventID: {record['eventID']}")
        logger.debug(f"eventName: {record['eventName']}")
        logger.debug("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))

    logger.debug('Successfully processed {} records.'.format(len(event['Records'])))
    return "Done"



def add_records(event, context):
    my_kwargs = event.get('kwargs')
    max_records = int(my_kwargs['max'])
    num_records_to_add = randint(1,max_records)
    logger.debug(f"*** DynamoDbEvents.add_records.max records: {num_records_to_add}")

    table = dynamodb.Table('zappa_stream_table')

    for record_index in range(1,num_records_to_add+1):
        # Generate a random string
        # with 32 characters.
        random_id = ''.join([choice(string.ascii_letters + string.digits) for n in range(32)])
        random_prefix = ''.join([choice(string.ascii_letters + string.digits) for n in range(8)])
        logger.debug(f"put_item: {random_id} with value: {random_prefix}")

        table.put_item(
            Item={
                'id': random_id,
                'payload': f'{random_prefix} This is the payload'
            }
        )

    return 'Done'
