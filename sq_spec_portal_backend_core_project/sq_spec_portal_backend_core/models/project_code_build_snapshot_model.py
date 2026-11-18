from django.contrib.auth.models import User
from django.db import models

from sq_spec_portal_backend_core.models.project_model import (
    ProjectModel,
)


class ProjectCodeBuildSnapshotModel(models.Model):
    """Represents a project code build snapshot."""

    build_status = models.CharField(max_length=255, null=True, blank=True)
    deploy_status = models.CharField(max_length=255, null=True, blank=True)
    github_event = models.CharField(max_length=255, null=True, blank=True)
    github_sha = models.CharField(max_length=255)
    project = models.ForeignKey(
        ProjectModel,
        related_name="project_code_build_snapshot_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    workflow_run_id = models.CharField(max_length=255, null=True, blank=True)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "project_code_build_snapshot"
        verbose_name_plural = "Project Code Build Snapshots"
        verbose_name = "Project Code Build Snapshot"
        app_label = "sq_spec_portal_backend_core"
