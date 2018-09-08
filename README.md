# Zappa Sandbox

Repo contains example code for working with Zappa

[Zappa](https://github.com/Miserlou/Zappa)


## AWS CLI

This project assumes you have the aws cli installed, and you setup your credentials.

if you have you will see a, *.aws* directory with a config and credentials files in it.

## zappa init

run this command to get an initial configuration file started.

## Flask Async

[Async Blog Post](https://blog.zappa.io/posts/capture-asynchronous-task-results)

Make sure you specify the name of the DynamoDB table name, to store response in.  The table does not have to exist ahead of time, you need to specify the name in the zappa config.

go to the /payload endpoint and the browser will keep reloading until the response is done.

### Zappa Settings
```
        "async_resources": true,
        "async_response_table": "flask_async_response",
        "async_response_table_read_capacity": 2,
        "async_response_table_write_capacity": 1,
        "timeout_seconds": 60

```

## Environments

zappa deploy flask_async
zappa update flask_async
zappa undeploy flask_async --remove-logs

## Zappa S3 Events

I believe the Zappa documentation is not quite right for this event type.

If you read here, [Executing in Response to AWS Events](https://github.com/Miserlou/Zappa#executing-in-response-to-aws-events)

you are led to believe that the *function* value should be the module.function_name to call when that particular event is fired.  However what I found in practice is that the *function* value is used in the name and description of the S3 event created, but the lambda function that is called is the one specfied in *lambda_handler*. 

Below when a file is uploaded to the pryan-landing bucket, then the lambda defined in S3Events.py, function *process_upload_function* will be called.

The ramification of this is that if you define another event, then it will call the same lambda.


```json
    "s3_env": {
        "aws_region": "us-east-1",
        "profile_name": "spr",
        "project_name": "s3_event_test",
        "runtime": "python3.6",
        "s3_bucket": "pryan-landing",
        "timeout_seconds": 60,
        "lambda_handler": "S3Events.process_upload_function",
        "use_apigateway": false,
        "events": [
            {
                "function": "s3_event_landing",
                "event_source": {
                    "arn": "arn:aws:s3:::pryan-landing",
                    "events": [
                        "s3:ObjectCreated:*"
                    ]
                }
            },
            {
                "function": "s3_event_staging",
                "event_source": {
                    "arn": "arn:aws:s3:::pryan-staging",
                    "events": [
                        "s3:ObjectCreated:*"
                    ]
                }
            }

        ]
    }

```

zappa deploy s3_events_env
zappa schedule s3_events_env
