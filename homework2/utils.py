import json
import boto3
import botocore.exceptions
import botocore.client

_credentials = {}


def camel_case_to_snake_case(string: str) -> str:
    result = ""
    for char in string:
        if char.isupper():
            result += "_" + char.lower()
        else:
            result += char
    return result


def validate_credentials() -> bool:
    return _credentials != {}


def list_ecs_clusters() -> dict:
    keys_to_keep = ["clusterName", "clusterArn", "status", "registeredContainerInstancesCount",
                    "runningTasksCount", "pendingTasksCount"]
    client = boto3.client(
        'ecs',
        region_name=_credentials["aws_region"],
        aws_access_key_id=_credentials["aws_access_key_id"],
        aws_secret_access_key=_credentials["aws_secret_access_key"],
    )
    response = client.list_clusters()
    if 'nextToken' in response:
        next_token = response['nextToken']
    else:
        next_token = None
    cluster_names = []
    while True:
        cluster_arns = response["clusterArns"]
        cluster_names.extend([arn.split('/')[1] for arn in cluster_arns])
        if next_token is None:
            break
        else:
            response = client.list_clusters(nextToekn=next_token)
            if 'nextToken' in response:
                next_token = response['nextToken']
            else:
                next_token = None
    response = client.describe_clusters(clusters=cluster_names)
    result = {"clusters": response["clusters"]}
    result["clusters"] = [
        {camel_case_to_snake_case(key): cluster[key] for key in keys_to_keep} for cluster in result["clusters"]
    ]
    return result


def list_ecs_services(cluster: str) -> dict:
    keys_to_keep = ["service_name", "service_arn", "status", "desired_count", "running_count",
                    "pending_count", "deployment_status"]
    client = boto3.client(
        'ecs',
        region_name=_credentials["aws_region"],
        aws_access_key_id=_credentials["aws_access_key_id"],
        aws_secret_access_key=_credentials["aws_secret_access_key"],
    )
    response = client.list_services(cluster=cluster)
    if 'nextToken' in response:
        next_token = response['nextToken']
    else:
        next_token = None
    service_names = []
    while True:
        service_arns = response["serviceArns"]
        service_names.extend([arn.split('/')[1] for arn in service_arns])
        if next_token is None:
            break
        else:
            response = client.list_services(cluster=cluster, nextToekn=next_token)
            if 'nextToken' in response:
                next_token = response['nextToken']
            else:
                next_token = None
    if not service_names:
        return {"services": []}
    response = client.describe_services(cluster=cluster, servicess=service_names)
    result = {"services": response["services"]}
    result["services"] = [
        {camel_case_to_snake_case(key): cluster[key] for key in keys_to_keep} for cluster in result["services"]
    ]
    return result


def initialize_credentials(access_key: str, secret_key: str, region: str) -> None:
    _credentials["aws_access_key_id"] = access_key
    _credentials["aws_secret_access_key"] = secret_key
    _credentials["aws_region"] = region


def delete_credentials() -> None:
    _credentials.clear()


if __name__ == "__main__":
    try:
        with open("auth.json", "r") as f:
            _credentials = json.load(f)
    except FileNotFoundError as e:
        print("No auth file located, please enter manually:")
        _credentials["aws_access_key_id"] = input("Please enter access key ID: ")
        _credentials["aws_secret_access_key"] = input("Please enter secret access key: ")
        _credentials["aws_region"] = input("Please enter AWS region: ")

    print(list_ecs_clusters())
