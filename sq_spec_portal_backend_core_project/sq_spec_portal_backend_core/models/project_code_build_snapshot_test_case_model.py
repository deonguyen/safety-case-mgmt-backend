from django.contrib.auth.models import User
from django.db import models

from sq_spec_portal_backend_core.models.project_model import (
    ProjectModel,
)
from sq_spec_portal_backend_core.models.specification_test_case_model import SpecificationTestCaseModel
from sq_spec_portal_backend_core.models.project_code_build_snapshot_model import ProjectCodeBuildSnapshotModel


class ProjectCodeBuildSnapshotTestCaseModel(models.Model):
    """Represents a project code build snapshot test case."""
    project_code_build_snapshot = models.ForeignKey(
        ProjectCodeBuildSnapshotModel,
        related_name="project_code_build_snapshot_test_case_project_code_build_snapshot_id_x_project_code_build_snapshot_id",
        on_delete=models.DO_NOTHING,
        db_column="project_code_build_snapshot_id",
    )

    project = models.ForeignKey(
        ProjectModel,
        related_name="project_code_build_snapshot_test_case_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    test_case = models.ForeignKey(
        SpecificationTestCaseModel,
        related_name="project_code_build_snapshot_test_case_test_case_id_x_test_case_id",
        on_delete=models.DO_NOTHING,
        db_column="test_case_id",
    )

    def __int__(self):
        return self.id

    class Meta:
        db_table = "project_code_build_snapshot_test_case"
        verbose_name_plural = "Project Code Build Snapshot Test Cases"
        verbose_name = "Project Code Build Snapshot Test Case"
        app_label = "sq_spec_portal_backend_core"
