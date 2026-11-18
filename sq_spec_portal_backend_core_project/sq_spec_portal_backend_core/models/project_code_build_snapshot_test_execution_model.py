from django.contrib.auth.models import User
from django.db import models

from sq_spec_portal_backend_core.models.project_model import (
    ProjectModel,
)
from sq_spec_portal_backend_core.models.specification_test_execution_model import SpecificationTestExecutionModel
from sq_spec_portal_backend_core.models.project_code_build_snapshot_model import ProjectCodeBuildSnapshotModel


class ProjectCodeBuildSnapshotTestExecutionModel(models.Model):
    """Represents a project code build snapshot test execution."""
    project_code_build_snapshot = models.ForeignKey(
        ProjectCodeBuildSnapshotModel,
        related_name="project_code_build_snapshot_test_execution_project_code_build_snapshot_id_x_project_code_build_snapshot_id",
        on_delete=models.DO_NOTHING,
        db_column="project_code_build_snapshot_id",
    )

    project = models.ForeignKey(
        ProjectModel,
        related_name="project_code_build_snapshot_test_execution_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    test_execution = models.ForeignKey(
        SpecificationTestExecutionModel,
        related_name="project_code_build_snapshot_test_execution_test_execution_id_x_test_execution_id",
        on_delete=models.DO_NOTHING,
        db_column="test_execution_id",
    )

    def __int__(self):
        return self.id

    class Meta:
        db_table = "project_code_build_snapshot_test_execution"
        verbose_name_plural = "Project Code Build Snapshot Test Executions"
        verbose_name = "Project Code Build Snapshot Test Execution"
        app_label = "sq_spec_portal_backend_core"
