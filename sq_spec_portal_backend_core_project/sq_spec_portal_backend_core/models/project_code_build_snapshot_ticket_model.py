from django.contrib.auth.models import User
from django.db import models

from sq_spec_portal_backend_core.models.project_model import (
    ProjectModel,
)
from sq_spec_portal_backend_core.models.project_code_build_snapshot_model import (
    ProjectCodeBuildSnapshotModel,
)

class ProjectCodeBuildSnapshotTicketModel(models.Model):
    """Represents a project code build snapshot ticket."""
    project_code_build_snapshot = models.ForeignKey(
        ProjectCodeBuildSnapshotModel,
        related_name="project_code_build_snapshot_ticket_project_code_build_snapshot_id_x_project_code_build_snapshot_id",
        on_delete=models.DO_NOTHING,
        db_column="project_code_build_snapshot_id",
    )

    project = models.ForeignKey(
        ProjectModel,
        related_name="project_code_build_snapshot_ticket_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    triggered_reference_id = models.CharField(max_length=255)
    triggered_source = models.TextField()
    triggered_time = models.DateTimeField()
    type = models.CharField(max_length=255)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "project_code_build_snapshot_ticket"
        verbose_name_plural = "Project Code Build Snapshot Tickets"
        verbose_name = "Project Code Build Snapshot Ticket"
        app_label = "sq_spec_portal_backend_core"
