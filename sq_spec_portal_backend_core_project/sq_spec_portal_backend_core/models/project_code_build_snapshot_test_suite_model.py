from django.contrib.auth.models import User
from django.db import models

from sq_spec_portal_backend_core.models.project_model import (
    ProjectModel,
)
from sq_spec_portal_backend_core.models.specification_test_suite_model import SpecificationTestSuiteModel
from sq_spec_portal_backend_core.models.project_code_build_snapshot_model import ProjectCodeBuildSnapshotModel


class ProjectCodeBuildSnapshotTestSuiteModel(models.Model):
    """Represents a project code build snapshot test suite."""
    project_code_build_snapshot = models.ForeignKey(
        ProjectCodeBuildSnapshotModel,
        related_name="project_code_build_snapshot_test_suite_project_code_build_snapshot_id_x_project_code_build_snapshot_id",
        on_delete=models.DO_NOTHING,
        db_column="project_code_build_snapshot_id",
    )

    project = models.ForeignKey(
        ProjectModel,
        related_name="project_code_build_snapshot_test_suite_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    test_suite = models.ForeignKey(
        SpecificationTestSuiteModel,
        related_name="project_code_build_snapshot_test_suite_test_suite_id_x_test_suite_id",
        on_delete=models.DO_NOTHING,
        db_column="test_suite_id",
    )

    def __int__(self):
        return self.id

    class Meta:
        db_table = "project_code_build_snapshot_test_suite"
        verbose_name_plural = "Project Code Build Snapshot Test Suites"
        verbose_name = "Project Code Build Snapshot Test Suite"
        app_label = "sq_spec_portal_backend_core"
