from django.contrib.auth.models import User
from django.db import models

from sq_spec_portal_backend_core.models.project_model import (
    ProjectModel,
)
from sq_spec_portal_backend_core.models.project_code_build_snapshot_model import (
    ProjectCodeBuildSnapshotModel,
)
from sq_spec_portal_backend_core.models.specification_model import (
    SpecificationModel,
)
from sq_spec_portal_backend_core.models.specification_revision_model import (
    SpecificationRevisionModel,
)


class ProjectCodeBuildSnapshotSpecificationModel(models.Model):
    """Represents a project code build snapshot specification."""

    project_code_build_snapshot = models.ForeignKey(
        ProjectCodeBuildSnapshotModel,
        related_name="project_code_build_snapshot_specification_project_code_build_snapshot_id_x_project_code_build_snapshot_id",
        on_delete=models.DO_NOTHING,
        db_column="project_code_build_snapshot_id",
    )
    project = models.ForeignKey(
        ProjectModel,
        related_name="project_code_build_snapshot_specification_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    specification = models.ForeignKey(
        SpecificationModel,
        related_name="project_code_build_snapshot_specification_specification_id_x_specification_id",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        db_column="specification_id",
    )
    specification_revision = models.ForeignKey(
        SpecificationRevisionModel,
        related_name="project_code_build_snapshot_specification_specification_revision_id_x_specification_revision_id",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        db_column="specification_revision_id",
    )

    def __int__(self):
        return self.id

    class Meta:
        db_table = "project_code_build_snapshot_specification"
        verbose_name_plural = "Project Code Build Snapshot Specifications"
        verbose_name = "Project Code Build Snapshot Specification"
        app_label = "sq_spec_portal_backend_core"
