import re
import json

"""
Example of how to add environment variables from a local file during deployment so that they do not have
to be part of the zappa_settings.json file.
"""

def settings_callback(zappa_cli):
    """
    after the settings have been read, potentially manipulate the base_url in the base.html file
    :param zappa_cli: reference to: https://github.com/Miserlou/Zappa/blob/master/zappa/cli.py
    :return:
    """
    print("settings callback called")
    print("***********************************************")
    print("Create .zappa.environment_variables.json with a json configuration, like zappa_settings to hold sensitive environments variables.")
    print("***********************************************")
    # print(zappa_cli.environment_variables)
    # print(zappa_cli.vargs)
    command = zappa_cli.vargs['command']
    stage_env = zappa_cli.vargs['stage_env']
    print(command, stage_env)

    # read zappa environment variables for the stage_env
    with open("./.zappa.environment_variables.json", "r") as f:
        env_json = json.loads(f.read())
        if stage_env in env_json:
            stage_env_json = env_json[stage_env]
            if "environment_variables" in stage_env_json:
                env_tuples = list((stage_env_json['environment_variables']).items())
                for env_tuple in env_tuples:
                    zappa_cli.environment_variables[env_tuple[0]] = env_tuple[1]
            if "aws_environment_variables" in stage_env_json:
                env_tuples = list((stage_env_json['aws_environment_variables']).items())
                for env_tuple in env_tuples:
                    zappa_cli.aws_environment_variables[env_tuple[0]] = env_tuple[1]


def post_callback(zappa_cli):
    """
    after the command completes, revert the base_url to an empty string so it can run locally.
    :param zappa_cli:
    :return:
    """

    print("post callback called")
    # print(zappa_cli)
    # print(zappa_cli.vargs)
    print(zappa_cli.environment_variables)

def zip_callback(zappa_cli):
    print("zip callback called")
    print(zappa_cli)
    print(zappa_cli.vargs)
    print(zappa_cli.environment_variables)
