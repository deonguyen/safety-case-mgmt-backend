import os
import time
import jwt
import requests
from django.core.cache import cache
import boto3


def get_ecs_metadata():
    # 1. Fetch the metadata URI from environment variables
    metadata_uri = os.environ.get("ECS_CONTAINER_METADATA_URI_V4")

    if not metadata_uri:
        print("Error: ECS_CONTAINER_METADATA_URI_V4 environment variable not found.")
        print(
            "Ensure this script is running inside an ECS task using platform version v1.4.0 or later."
        )
        return None

    try:
        # 2. Query the /task endpoint for ARN details
        response = requests.get(f"{metadata_uri}/task", timeout=2)
        response.raise_for_status()
        task_metadata = response.json()

        # 3. Extract Cluster and TaskARN
        # The 'Cluster' property usually returns either the short name or full ARN
        cluster_arn_or_name = task_metadata.get("Cluster", "")
        task_arn = task_metadata.get("TaskARN", "")

        # 4. Parse the short names out of the ARNs
        # ARNs look like: arn:aws:ecs:region:aws_account_id:task/cluster_name/task_id
        cluster_name = cluster_arn_or_name.split("/")[-1]
        task_id = task_arn.split("/")[-1]

        # print(f"Cluster name: {cluster_name}")
        # print(f"Task ID: {task_id}")
        # print(f"Task ARN: {task_arn}")

        return {"cluster_name": cluster_name, "task_id": task_id, "task_arn": task_arn}

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to metadata endpoint: {e}")
        return None


def get_fargate_task_ips():
    ecs_client = boto3.client("ecs")
    ec2_client = boto3.client("ec2")

    ecs_meta_data = get_ecs_metadata()

    cluster_name = ecs_meta_data.get("cluster_name")
    task_arn = ecs_meta_data.get("task_arn")

    print(f"Cluster name: {cluster_name}")
    print(f"Task ID: {ecs_meta_data.get("task_id")}")
    print(f"Task ARN: {task_arn}")

    # 1. Describe the ECS task to look up network attachments
    ecs_response = ecs_client.describe_tasks(cluster=cluster_name, tasks=[task_arn])

    if not ecs_response["tasks"]:
        raise ValueError(f"No task found for ARN: {task_arn}")

    task = ecs_response["tasks"][0]

    # 2. Extract the ENI ID and Private IP from the task attachments
    eni_id = None
    private_ip = None

    for attachment in task.get("attachments", []):
        if attachment.get("type") == "ElasticNetworkInterface":
            for detail in attachment.get("details", []):
                if detail.get("name") == "networkInterfaceId":
                    eni_id = detail.get("value")
                if detail.get("name") == "privateIPv4Address":
                    private_ip = detail.get("value")

    if not eni_id:
        raise ValueError(
            "Could not find an Elastic Network Interface (ENI) attached to this task."
        )

    # 3. Use the ENI ID to fetch the Public IP from EC2
    ec2_response = ec2_client.describe_network_interfaces(NetworkInterfaceIds=[eni_id])

    eni_details = ec2_response["NetworkInterfaces"][0]

    # Public IP will only exist if "Auto-assign public IP" was enabled and it's in a public subnet
    public_ip = eni_details.get("Association", {}).get(
        "PublicIp", "No Public IP assigned"
    )

    print(f"Private IP: {private_ip}")
    print(f"Public IP: {public_ip}")

    return {"private_ip": private_ip, "public_ip": public_ip}


def get_github_app_installation_token(
    github_app_id: int, github_app_installation_id: int
):
    """
    Generates a GitHub App installation token.
    It caches the token to avoid regenerating it on every request.
    """
    cached_token = cache.get("github_installation_token")
    if cached_token:
        return cached_token

    # get_fargate_task_ips()
    
    github_app_private_key = os.environ.get("GITHUB_APP_PRIVATE_KEY_PEM")
    # 1. Generate JWT
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),  # 10 minutes expiration
        "iss": str(github_app_id),
    }

    try:
        github_jwt = jwt.encode(payload, github_app_private_key, algorithm="RS256")
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

    # 2. Get Installation Access Token
    headers = {
        "Authorization": f"Bearer {github_jwt}",
        "Accept": "application/vnd.github.v3+json",
    }
    url = f"https://api.github.com/app/installations/{github_app_installation_id}/access_tokens"

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        token = token_data.get("token")
        cache.set(
            "github_installation_token", token, timeout=3500
        )  # Cache for just under an hour
        return token
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response details: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return None
