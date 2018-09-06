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

make sure to deploy the configuation first, then schedule

zappa deploy s3_events_env
zappa schedule s3_events_env
