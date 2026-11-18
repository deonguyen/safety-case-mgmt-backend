from django.db import models

from sq_spec_portal_backend_core.models.project_model import ProjectModel


class SpecificationModel(models.Model):
    """Represents a specification created by a user."""

    code = models.CharField(max_length=500)
    content = models.TextField(
        null=True,
        blank=True,
    )
    interface = models.TextField(
        null=True,
        blank=True,
    )
    interface_diagram = models.TextField(
        null=True,
        blank=True,
    )
    req_id = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column="req_id",
    )
    dependencies = models.TextField(
        null=True,
        blank=True,
    )
    global_id = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        db_column="global_id",
    )
    name = models.CharField(max_length=500)
    path = models.TextField(
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        ProjectModel,
        related_name="specification_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )
    raw_content = models.TextField(
        null=True,
        blank=True,
    )
    source = models.TextField(
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    type = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
    latest_version = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.code

    class Meta:
        db_table = "specification"
        verbose_name_plural = "Specifications"
        verbose_name = "Specification"
        app_label = "sq_spec_portal_backend_core"
