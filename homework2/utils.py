import json
import boto3


def initialize_session(credentials: dict) -> boto3.session.Session:
    return boto3.session.Session(
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=credentials["aws_region"],
    )


if __name__ == "__main__":
    try:
        with open("auth.json", "r") as f:
            credentials = json.load(f)
    except FileNotFoundError as e:
        print("No auth file located, please enter manually:")
        credentials["aws_access_key_id"] = input("Please enter access key ID: ")
        credentials["aws_secret_access_key"] = input("Please enter secret access key: ")
        credentials["aws_region"] = input("Please enter AWS region: ")

    session = initialize_session(credentials)
    ecs = session.client('ecs')
    response = ecs.describe_clusters()
    print(response)
