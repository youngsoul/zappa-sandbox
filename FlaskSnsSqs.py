from zappa.async import task, get_async_response
from flask import Flask, make_response, abort, url_for, redirect, request, jsonify
from time import sleep
import os
import boto3

app = Flask(__name__)

"""
FlaskSns

Flask app to publish a message to an Sns topic
"""

def send_to_sns(subject, message, aws_sns_arn):
    print("Sending notification to: %s" % aws_sns_arn)

    client = boto3.client('sns')

    response = client.publish(
        TargetArn=aws_sns_arn,
        Message=message,
        Subject=subject)

    if 'MessageId' in response:
        print("Notification sent with message id: %s" % response['MessageId'])
    else:
        print("Sending notification failed with response: %s" % str(response))

@app.route('/sns', methods=['POST'])
def sns():
    print("sns...")
    aws_sns_arn = os.environ['SNS_ARN'] if 'SNS_ARN' in os.environ else None
    if aws_sns_arn is None:
        return

    send_to_sns("test subject", "test message", aws_sns_arn)

    return f"Message send to sns arn: {aws_sns_arn}", 200


@task()
def sns_publish(delay):
    print(f"FlaskAsync  longrunner sleeping...: {delay}")
    sleep(delay)
    print("FlaskAsync longrunner returning....")
    return {'MESSAGE': "It took {} seconds to generate this.".format(delay)}
