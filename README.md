# Zappa Sandbox

Repo contains example code for working with Zappa

[Zappa](https://github.com/Miserlou/Zappa)

## Gotchas

- You cannot exclude *docs* directory.  If you exclude the docs directory, the WSGI lambda wont deploy and the log will have the follow error message:

*Unable to import module 'handler': No module named 'botocore.docs'*


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

For S3 events to work, you **CANNOT** include the lambda_handler in the config.  By leaving this out, Zappa will install its own default lambda implementation that will handle the functions for the events.



```json
    "s3_env": {
        "aws_region": "us-east-1",
        "profile_name": "spr",
        "project_name": "s3_event_test",
        "runtime": "python3.6",
        "s3_bucket": "pryan-landing",
        "timeout_seconds": 60,
        "use_apigateway": false,
        "events": [
            {
                "function": "S3Events.process_upload_function",
                "event_source": {
                    "arn": "arn:aws:s3:::pryan-landing",
                    "events": [
                        "s3:ObjectCreated:*"
                    ]
                }
            },
            {
                "function": "S3Events.process_upload_function2",
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

zappa deploy s3_env

### Zappa Recurring Events

Create a Lambda deployment that will be called every 'n' minutes

[Rate Expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#RateExpressions)

```json
    "recurring_env": {
        "aws_region": "us-east-1",
        "profile_name": "spr",
        "project_name": "recurring_event_test",
        "runtime": "python3.6",
        "s3_bucket": "pryan-landing",
        "timeout_seconds": 120,
        "use_apigateway": false,
        "xray_tracing": true,
        "events": [
            {
                "function": "RecurringEvents.recurring_event_handler",
                "kwargs": {"key1": "value1", "key2": "value2"},
                "expression": "rate(1 minute)"
            },
            {
                "function": "RecurringEvents.every_2_mins",
                "kwargs": {"key1": "value1", "key2": "value2"},
                "expression": "rate(2 minutes)"
            }
        ]
    }

```

Deploy will deploy and start the schedule
* zappa deploy recurring_env

Schedule will unschedule a currently scheduled deployment, and reschdule or restart an unscheduled deployment
* zappa schedule recurring_env

Unschedule will stop or unschedule a currently scheduled deployment but will **not** undeploy the deployment.  You can then call *schedule* to reschedule the existing deployment
* zappa unschedule recurring_env

Undeploy will undeploy, and unschedule, an existing deployed service
* zappa undeploy recurring_env --remove-logs

### Zappa DynamoDB Streams

[AWS Shard Iterator Type](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_GetShardIterator.html#API_streams_GetShardIterator_RequestSyntax)

* TRIM_HORIZON - Start reading at the last (untrimmed) stream record, which is the oldest record in the shard. In DynamoDB Streams, there is a 24 hour limit on data retention. Stream records whose age exceeds this limit are subject to removal (trimming) from the stream.

* LATEST - Start reading just after the most recent stream record in the shard, so that you always read the most recent data in the shard.


First, create a DynamoDB Table, and enable streaming.  This will provide the streaming ARN, that you use in the zappa_settings.json file.

For this example, give the key value a name of 'id'

This example creates one event listener for scheduled, recurring events that will add records to a dynamodb table and the other is listening to the dynamodb stream for records being added.

```json
    "dynamo_env": {
        "aws_region": "us-east-1",
        "profile_name": "spr",
        "project_name": "dynamo_event_test",
        "runtime": "python3.6",
        "s3_bucket": "pryan-landing",
        "timeout_seconds": 120,
        "use_apigateway": false,
        "xray_tracing": true,
        "events": [
            {
                "function": "DynamoDbEvents.dynamo_events",
                "event_source": {
                    "arn":  "arn:aws:dynamodb:us-east-1:485071734737:table/zappa_stream_table/stream/2018-09-10T03:11:38.835",
                    "starting_position": "TRIM_HORIZON", // Supported values: TRIM_HORIZON, LATEST
                    "batch_size": 50, // Max: 1000
                    "enabled": true // Default is false
               }
            },
            {
                "function": "DynamoDbEvents.add_records",
                "kwargs": {"max": "50"},
                "expression": "rate(1 minute)"
            }

        ]
    }

```
