import os
import threading

from django.db import close_old_connections
from sq_spec_portal_backend_core.models import (
    NotificationModel,
    ProjectModel,
    ProjectSpecificationModel,
    SpecificationRevisionModel,
    CodeImplementationTraceModel,
    CodeImplementationTraceLogModel,
)
from sq_spec_portal_backend_spec.services import github_app_service, github_service
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
import re
import requests
from django.contrib.auth.models import User


class ImportTraceabilityViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"])
    def import_traceability_for_repos(self, request):
        project_id = request.data.get("project_id")
        github_url = request.data.get("github_url")

        try:
            project = ProjectModel.objects.get(pk=project_id)
        except ProjectModel.DoesNotExist:
            return Response(
                {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
            )

        def run_import_traceability_for_repos(project, github_url, user):
            try:
                close_old_connections()
                result = github_service.process_import_traceability_for_repos(
                    project,
                    github_url,
                    user,
                )
                if isinstance(result, Response):
                    error_msg = (
                        result.data.get("error", "Unknown error")
                        if hasattr(result, "data")
                        else "Unknown error"
                    )
                    raise Exception(error_msg)

                created_count = result
                active_users = User.objects.filter(is_active=True)
                notifications = [
                    NotificationModel(
                        user=u,
                        title="JAMA Import Successful",
                        message=f"Successfully synced and created {created_count} new specifications from JAMA for project '{project.name}'.",
                    )
                    for u in active_users
                ]
                NotificationModel.objects.bulk_create(notifications)
                print(
                    f"Successfully synced and created {created_count} new specifications from JAMA for project '{project.name}'."
                )
            except Exception as e:
                NotificationModel.objects.create(
                    user=user,
                    title="JAMA Import Failed",
                    message=f"Failed to sync specifications from JAMA for project '{project.name}'. Error: {str(e)}",
                )
            finally:
                close_old_connections()

        thread = threading.Thread(
            target=run_import_traceability_for_repos,
            args=(
                project,
                github_url,
                request.user,
            ),
        )
        thread.start()

        return Response(
            {
                "message": "GitHub import has been started in the background. You will be notified upon completion."
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def import_traceability_from_repos_code_search(self, request):
        project_id = request.data.get("project_id")
        github_url = request.data.get("github_url")

        try:
            project = ProjectModel.objects.get(pk=project_id)
        except ProjectModel.DoesNotExist:
            return Response(
                {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
            )

        def run_import_traceability_from_repos_code_search(project, github_url, user):
            try:
                close_old_connections()
                result = (
                    github_service.process_import_traceability_from_repos_code_search(
                        project,
                        github_url,
                        user,
                    )
                )
                if isinstance(result, Response):
                    error_msg = (
                        result.data.get("error", "Unknown error")
                        if hasattr(result, "data")
                        else "Unknown error"
                    )
                    raise Exception(error_msg)

                created_count = result
                active_users = User.objects.filter(is_active=True)
                notifications = [
                    NotificationModel(
                        user=u,
                        title="JAMA Import Successful",
                        message=f"Successfully synced and created {created_count} new specifications from JAMA for project '{project.name}'.",
                    )
                    for u in active_users
                ]
                NotificationModel.objects.bulk_create(notifications)
                print(
                    f"Successfully synced and created {created_count} new specifications from JAMA for project '{project.name}'."
                )
            except Exception as e:
                NotificationModel.objects.create(
                    user=user,
                    title="JAMA Import Failed",
                    message=f"Failed to sync specifications from JAMA for project '{project.name}'. Error: {str(e)}",
                )
            finally:
                close_old_connections()

        thread = threading.Thread(
            target=run_import_traceability_from_repos_code_search,
            args=(
                project,
                github_url,
                request.user,
            ),
        )
        thread.start()

        return Response(
            {
                "message": "GitHub import has been started in the background. You will be notified upon completion."
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def import_traceability_from_repos_pr_search(self, request):
        project_id = request.data.get("project_id")
        github_url = request.data.get("github_url")

        try:
            project = ProjectModel.objects.get(pk=project_id)
        except ProjectModel.DoesNotExist:
            return Response(
                {"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND
            )

        def run_import_traceability_from_repos_pr_search(project, github_url, user):
            try:
                close_old_connections()
                result = (
                    github_service.process_import_traceability_from_repos_pr_search(
                        project,
                        github_url,
                        user,
                    )
                )
                if isinstance(result, Response):
                    error_msg = (
                        result.data.get("error", "Unknown error")
                        if hasattr(result, "data")
                        else "Unknown error"
                    )
                    raise Exception(error_msg)

                created_count = result
                active_users = User.objects.filter(is_active=True)
                notifications = [
                    NotificationModel(
                        user=u,
                        title="JAMA Import Successful",
                        message=f"Successfully synced and created {created_count} new specifications from JAMA for project '{project.name}'.",
                    )
                    for u in active_users
                ]
                NotificationModel.objects.bulk_create(notifications)
                print(
                    f"Successfully synced and created {created_count} new specifications from JAMA for project '{project.name}'."
                )
            except Exception as e:
                NotificationModel.objects.create(
                    user=user,
                    title="JAMA Import Failed",
                    message=f"Failed to sync specifications from JAMA for project '{project.name}'. Error: {str(e)}",
                )
            finally:
                close_old_connections()

        thread = threading.Thread(
            target=run_import_traceability_from_repos_pr_search,
            args=(
                project,
                github_url,
                request.user,
            ),
        )
        thread.start()

        return Response(
            {
                "message": "GitHub import has been started in the background. You will be notified upon completion."
            },
            status=status.HTTP_202_ACCEPTED,
        )
