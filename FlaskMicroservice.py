from flask import Flask, request, jsonify
import logging
import boto3
from datetime import datetime
import json

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "Congratulations! Flask Microservice Deployed!"

# here is how we are handling routing with flask:
@app.route('/flask_microservice/user', methods=['POST'])
def user_create():
    logger.debug("FlaskSimple.index: debug message")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('zappa-microservice')

    if request.json:
        username = request.json['username']
        password = request.json['password']
        email = request.json['emailaddress']
        response = table.put_item(
            Item={
                'email': email,
                'info': {
                    'username': username,
                    'password': password,
                    'created': "{:%B %d, %Y}".format(datetime.now())
                }
            }
        )

        print("PutItem succeeded:")
        print(json.dumps(response, indent=4))

    return jsonify(json.dumps(response, indent=4)), 200


@app.route('/flask_microservice/user/<email>', methods=['GET'])
def user_get(email):
    logger.debug("FlaskSimple.index: debug message")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('zappa-microservice')

    response = table.get_item(
        Key={
            'email': email
        }
    )

    print("GetItem succeeded:")
    print(json.dumps(response, indent=4))

    return jsonify(json.dumps(response, indent=4)), 200

# include this for local dev

if __name__ == '__main__':
    boto3.setup_default_session(profile_name='spr')

    app.run()