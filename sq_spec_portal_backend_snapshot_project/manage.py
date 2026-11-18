#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
from pathlib import Path


def main():
    """Run administrative tasks."""
    
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
    except ImportError:
        load_dotenv = None

    if load_dotenv:
        env_path = BASE_DIR / ".env"
        if env_path.is_file():
            print(f"--- Start of .env file content from {env_path} ---")
            with open(env_path, "r") as f:
                for line in f:
                    print(line.strip())
            print("--- End of .env file content ---")

        load_dotenv(env_path)

    
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "sq_spec_portal_backend_snapshot_project.settings"
    )
    try:
        from django.core.management.commands.runserver import Command as runserver

        # aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
        # aws_access_key = os.environ.get("AWS_ACCESS_KEY")
        # aws_access_secret = os.environ.get("AWS_ACCESS_SECRET")
        # aws_default_region = os.environ.get("AWS_DEFAULT_REGION")
        # aws_secrets_to_settings = os.environ.get("AWS_SECRETS_TO_SETTINGS")

        # print("aws_account_id: " + str(aws_account_id))
        # print("aws_access_key: " + str(aws_access_key))
        # print("aws_access_secret: " + str(aws_access_secret))
        # print("aws_default_region: " + str(aws_default_region))
        # print("aws_secrets_to_settings: " + str(aws_secrets_to_settings))

        # from sq_spec_portal_backend_snapshot.services.aws_secrets import get_aws_secret

        # # Load database connection from AWS Secrets Manager.
        # aws_secrets_to_settings_values = get_aws_secret(
        #     aws_access_key=aws_access_key,
        #     aws_access_secret=aws_access_secret,
        #     aws_region=aws_default_region,
        #     secret_id=aws_secrets_to_settings,
        # )

        # aws_secret_key_snapshot_settings = aws_secrets_to_settings_values.get(
        #     "SNAPSHOT_SETTINGS", {}
        # )

        # print(
        #     "aws_secret_key_snapshot_settings" + str(aws_secret_key_snapshot_settings)
        # )

        # snapshot_settings = get_aws_secret(
        #     aws_access_key=aws_access_key,
        #     aws_access_secret=aws_access_secret,
        #     aws_region=aws_default_region,
        #     secret_id=aws_secret_key_snapshot_settings,
        # )

        # runserver.default_port = snapshot_settings.get("DJANGO_RUNSERVER_PORT", {})
        # runserver.default_addr = "0.0.0.0"
        runserver.default_port =5004

        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
