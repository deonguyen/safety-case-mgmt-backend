"""Fetch secrets from AWS Secrets Manager and export them into os.environ."""

import json
import logging
import os

logger = logging.getLogger(__name__)


def get_aws_secret(
    aws_access_key: str,
    aws_access_secret: str,
    aws_region: str,
    secret_id: str,
):
    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError
    except ImportError:
        logger.warning("boto3 not installed; skipping AWS Secrets Manager load")
        return {}

    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_access_secret,
        region_name=aws_region,
    )

    client = session.client("secretsmanager")

    try:
        response = client.get_secret_value(SecretId=secret_id)
    except (BotoCoreError, ClientError) as exc:
        logger.error("Failed to fetch secret %s from AWS: %s", secret_id, exc)
        return {}

    raw = response.get("SecretString")
    if raw is None:
        logger.error("Secret %s has no SecretString payload", secret_id)
        return {}

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        logger.error("Secret %s is not valid JSON", secret_id)
        return {}

    if not isinstance(payload, dict):
        logger.error("Secret %s must be a JSON object at the top level", secret_id)
        return {}

    loaded = {}
    for key, value in payload.items():
        loaded[key] = value

    logger.info("Loaded %d keys from AWS secret %s", len(loaded), secret_id)
    return loaded
