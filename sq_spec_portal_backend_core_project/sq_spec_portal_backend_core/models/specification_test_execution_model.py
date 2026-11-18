from django.db import models


class SpecificationTestExecutionModel(models.Model):
    project = models.ForeignKey(
        "ProjectModel",
        related_name="specification_test_execution_project_id_x_project_id",
        on_delete=models.DO_NOTHING,
        db_column="project_id",
    )

    test_suite = models.ForeignKey(
        "SpecificationTestSuiteModel",
        related_name="specification_test_execution_test_suite_id_x_test_suite_id",
        on_delete=models.DO_NOTHING,
        db_column="test_suite_id",
    )

    test_case = models.ForeignKey(
        "SpecificationTestCaseModel",
        related_name="specification_test_execution_test_case_id_x_test_case_id",
        on_delete=models.DO_NOTHING,
        db_column="test_case_id",
    )

    test_result = models.CharField(max_length=255, null=True, blank=True)

    def __int__(self):
        return self.id

    class Meta:
        db_table = "specification_test_execution"
        verbose_name_plural = "Specification Test Executions"
        verbose_name = "Specification Test Execution"
        app_label = "sq_spec_portal_backend_core"
