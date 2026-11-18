import os
from rest_framework import viewsets
import json
import threading
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import close_old_connections
from rest_framework.decorators import action

from django.contrib.auth.models import User
from sq_spec_portal_backend_core.models import NotificationModel, ProjectModel

from sq_spec_portal_backend_snapshot.apps import SqSpecPortalBackendSnapshotConfig
from sq_spec_portal_backend_snapshot.services import snapshot_service


class WebhookViewSet(viewsets.ViewSet):

    @csrf_exempt
    @action(detail=False, methods=["post"])
    def github_webhook(self, request):
        """
        Receives webhook events from GitHub.
        """
        if request.method != "POST":
            return HttpResponse("Method Not Allowed", status=405)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Bad Request: Invalid JSON", status=400)

        github_event = data.get("github_event")
        workflow_run_id = data.get("workflow_run_id")
        build_status = data.get("build_status")
        deploy_status = data.get("deploy_status")
        github_sha = data.get("github_sha")
        webhook_secret = data.get("webhook_secret")
        project_id = data.get("project_id")

        print(f"Received GitHub webhook with SHA: {github_sha}")

        if webhook_secret != SqSpecPortalBackendSnapshotConfig.WEBHOOK_SECRET:
            return HttpResponse("Forbidden: Invalid webhook secret", status=403)

        def run_snapshot_process(
            build_status,
            deploy_status,
            github_event,
            github_sha,
            project_id,
            workflow_run_id,
        ):
            try:
                close_old_connections()
                project = ProjectModel.objects.get(id=project_id)
                snapshot_service.process_code_build_snapshot(
                    build_status,
                    deploy_status,
                    github_event,
                    github_sha,
                    project_id,
                    workflow_run_id,
                )
                print(f"Successfully processed snapshot for SHA: {github_sha}")

                active_users = User.objects.filter(is_active=True)
                notifications = [
                    NotificationModel(
                        user=u,
                        title="Snapshot Process Successful",
                        message=f"Successfully processed snapshot for project '{project.name}' with SHA: {github_sha}.",
                    )
                    for u in active_users
                ]
                NotificationModel.objects.bulk_create(notifications)

            except Exception as e:
                print(f"Failed to process snapshot for SHA {github_sha}: {e}")
                try:
                    project = ProjectModel.objects.get(id=project_id)
                    project_name = project.name
                except ProjectModel.DoesNotExist:
                    project_name = f"ID {project_id}"

                active_users = User.objects.filter(is_active=True)
                notifications = [
                    NotificationModel(
                        user=u,
                        title="Snapshot Process Failed",
                        message=f"Failed to process snapshot for project '{project_name}' with SHA {github_sha}. Error: {str(e)}",
                    )
                    for u in active_users
                ]
                NotificationModel.objects.bulk_create(notifications)
            finally:
                close_old_connections()

        thread = threading.Thread(
            target=run_snapshot_process,
            args=(
                build_status,
                deploy_status,
                github_event,
                github_sha,
                project_id,
                workflow_run_id,
            ),
        )
        thread.start()

        return JsonResponse(
            {
                "message": "Snapshot process started in the background.",
                "github_sha": github_sha,
            },
            status=202,
        )
