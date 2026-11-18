import os
import requests
import boto3
from django.utils import timezone
from botocore.exceptions import NoCredentialsError
from sq_spec_portal_backend_core.models import (
    ProjectCodeBuildSnapshotModel,
    ProjectCodeBuildSnapshotSpecificationModel,
    ProjectCodeBuildSnapshotTestSuiteModel,  # Assuming this new model exists
    ProjectCodeBuildSnapshotTestCaseModel,  # Assuming this new model exists
    ProjectModel,
    ProjectSpecificationModel,
    SpecificationModel,
    SpecificationRevisionModel,
    SpecificationTestCaseModel,
    SpecificationTestSuiteModel,
)
from sq_spec_portal_backend_snapshot.apps import SqSpecPortalBackendSnapshotConfig


def process_code_build_snapshot(
    build_status,
    deploy_status,
    github_event,
    github_sha,
    project_id,
    workflow_run_id,
):
    # Get project
    project = ProjectModel.objects.get(id=project_id)

    code_build_snapshot, created = (
        ProjectCodeBuildSnapshotModel.objects.update_or_create(
            project=project,
            github_sha=github_sha,
            defaults={
                "build_status": build_status,
                "deploy_status": deploy_status,
                "github_event": github_event,
                "workflow_run_id": workflow_run_id,
            },
        )
    )

    project_specifications = ProjectSpecificationModel.objects.filter(project=project)
    for project_specification in project_specifications:
        # Assuming project_specification.specification is already the SpecificationModel instance
        specification = project_specification.specification
        if not specification:
            continue

        specification_revision = SpecificationRevisionModel.objects.filter(
            project=project,
            specification=specification,
        ).first()
        if not specification_revision:
            continue

        project_code_build_snapshot_specification, created_spec_snapshot = (
            ProjectCodeBuildSnapshotSpecificationModel.objects.update_or_create(
                project_code_build_snapshot=code_build_snapshot,
                project=project,
                specification=specification,
                specification_revision=specification_revision,
            )
        )

        # Process test suites for this specification revision
        specification_test_suites = SpecificationTestSuiteModel.objects.filter(
            specification_revision=specification_revision
        )

        for test_suite in specification_test_suites:
            project_code_build_snapshot_test_suite, created_test_suite_snapshot = (
                ProjectCodeBuildSnapshotTestSuiteModel.objects.update_or_create(
                    project_code_build_snapshot_specification=project_code_build_snapshot_specification,
                    specification_test_suite=test_suite,
                    defaults={},
                )
            )

            # Process test cases for the current test suite
            specification_test_cases = SpecificationTestCaseModel.objects.filter(
                specification_test_suite=test_suite
            )

            for test_case in specification_test_cases:
                ProjectCodeBuildSnapshotTestCaseModel.objects.update_or_create(
                    project_code_build_snapshot_test_suite=project_code_build_snapshot_test_suite,
                    specification_test_case=test_case,
                    defaults={},
                )

    # # Download static code analysis CSV and upload to S3
    # csv_url = SqSpecPortalBackendSnapshotConfig.STATIC_ANALYSIS_CSV_URL
    # s3_bucket = SqSpecPortalBackendSnapshotConfig.AWS_STORAGE_BUCKET_NAME

    # if csv_url and s3_bucket:
    #     try:
    #         response = requests.get(csv_url, stream=True)
    #         response.raise_for_status()

    #         # Construct a unique file name for S3
    #         s3_file_name = f"snapshots/{project_id}/{github_sha}/static-analysis.csv"

    #         s3_client = boto3.client(
    #             "s3",
    #             aws_access_key_id=SqSpecPortalBackendSnapshotConfig.AWS_ACCESS_KEY_ID,
    #             aws_secret_access_key=SqSpecPortalBackendSnapshotConfig.AWS_SECRET_ACCESS_KEY,
    #             region_name=SqSpecPortalBackendSnapshotConfig.AWS_S3_REGION_NAME,
    #         )

    #         # Upload the file directly from the stream
    #         s3_client.upload_fileobj(response.raw, s3_bucket, s3_file_name)

    #         print(f"Successfully uploaded {s3_file_name} to S3 bucket {s3_bucket}")

    #     except requests.exceptions.RequestException as e:
    #         print(f"Failed to download CSV from {csv_url}: {e}")
    #     except NoCredentialsError:
    #         print("AWS credentials not available. Skipping S3 upload.")
    #     except Exception as e:
    #         print(f"An error occurred during S3 upload: {e}")

    return code_build_snapshot
