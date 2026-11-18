from django.db import models


class JamaItemTypeModel(models.Model):
    """Represents a priority created by a user."""

    description = models.TextField(blank=True)
    display = models.CharField(max_length=255)
    jama_item_type_id = models.IntegerField(null=True, blank=True)
    jama_project_id = models.IntegerField(null=True, blank=True)
    type_key = models.CharField(max_length=255)

    def __str__(self):
        return self.type_key

    class Meta:
        db_table = "jama_item_type"
        verbose_name_plural = "Jama Item Types"
        verbose_name = "Jama Item Type"
        app_label = "sq_spec_portal_backend_core"
        constraints = [
            models.UniqueConstraint(
                fields=["jama_item_type_id", "jama_project_id", "type_key"],
                name="unique_jama_project_item_type",
            )
        ]
