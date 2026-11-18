from django.contrib.auth.models import User
from django.db import models

from sq_spec_portal_backend_core.models.project_model import (
    ProjectModel,
)
from sq_spec_portal_backend_core.models.project_code_build_snapshot_model import (
    ProjectCodeBuildSnapshotModel,
)

class ProjectCodeBuildSnapshotAnalysisModel(models.Model):
    """Represents a project code build snapshot analysis."""
    project_code_build_snapshot = models.ForeignKey(
        ProjectCodeBuildSnapshotModel,
        related_name="project_code_build_snapshot_analysis_project_code_build_snapshot_id_x_project_code_build_snapshot_id",
        on_delete=models.DO_NOTHING,
        db_column="project_code_build_snapshot_id",
    )

    project = models.ForeignKey(
        ProjectModel,
        related_name="project_code_build_snapshot_analysis_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    static_analysis_path = models.TextField()

    def __int__(self):
        return self.id

    class Meta:
        db_table = "project_code_build_snapshot_analysis"
        verbose_name_plural = "Project Code Build Snapshot Analyses"
        verbose_name = "Project Code Build Snapshot Analysis"
        app_label = "sq_spec_portal_backend_core"
