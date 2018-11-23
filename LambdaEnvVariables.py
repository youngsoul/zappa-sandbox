import os
import logging
import boto3
from base64 import b64decode


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

"""
This Lambda is used to demonstrate how to set and access environment variables in a lambda deployed by Zappa

Environment variable values can only be strings.

There are:

Local Environment Variables
- not visible on the AWS Lambda management console but available via os.environ.get('name')

Remote AWS Environment Variables
- ARE visible on the AWS Lambda management console


zappa tail lambda_env_variables

zappa invoke lambda_env_variables 'LambdaEnvVariables.lambda_handler'


setting up kms key master: https://www.youtube.com/watch?v=LvCmp3lRu_4
Your customer master key was created with alias zappa-test-key and key ID 88c40b4b-cfae-4d1d-bdb4-ca652a2930c0


Your customer master key was created with alias zappa-test-key2 and key ID 609264a5-b25c-4938-9e06-361d4d1713ce

To encrypt environment variables:
aws kms encrypt --key-id arn:aws:kms:us-east-1:485071734737:key/609264a5-b25c-4938-9e06-361d4d1713ce --plaintext "zappa encrypted env variable value 1" --output text --profile spr --query CipherTextBlob | base64  > kms_env_var2.b64

aws kms decrypt --ciphertext-blob file://kms_env_var2.b64 --output text --profile spr --query Plaintext | base64 --decode
"""


def lambda_handler(event, context):
    logger.debug("In LambdaEnvVariables.lambda_handler")


    logger.debug("------ Zappa Provided Environment Variables ----")
    env_name = 'SERVERTYPE'
    if env_name in os.environ:
        env_value=os.environ.get(env_name)
        logger.debug(f"{env_name}: {env_value}")

    env_name = 'FRAMEWORK'
    if env_name in os.environ:
        env_value=os.environ.get(env_name)
        logger.debug(f"{env_name}: {env_value}")

    env_name = 'PROJECT'
    if env_name in os.environ:
        env_value=os.environ.get(env_name)
        logger.debug(f"{env_name}: {env_value}")

    env_name = 'STAGE'
    if env_name in os.environ:
        env_value=os.environ.get(env_name)
        logger.debug(f"{env_name}: {env_value}")

    value1 = os.environ.get('key1')
    value2 = os.environ.get('key2')
    value3 = os.environ.get('key3')

    logger.debug("------ Local Environment Variables ----")
    logger.debug(f"key1: {value1}")
    logger.debug(f"key2: {value2}")
    logger.debug(f"key3: {value3}")

    logger.debug("------ AWS Environment Variables ----")
    logger.debug(f"aws_key1: {os.environ.get('aws_key1')}")
    logger.debug(f"aws_key2: {os.environ.get('aws_key2')}")

    logger.debug("------ Callback Added Local Environment Variables ----")
    logger.debug(f"callback_key1: {os.environ.get('callback_key1')}")
    logger.debug(f"callback_key2: {os.environ.get('callback_key2')}")
    logger.debug(f"callback_key3: {os.environ.get('callback_key3')}")

    logger.debug("------ AWS Environment Variables ----")
    logger.debug(f"callback_aws_key1: {os.environ.get('callback_aws_key1')}")
    logger.debug(f"callback_aws_key2: {os.environ.get('callback_aws_key2')}")

