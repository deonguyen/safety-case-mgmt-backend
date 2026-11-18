from rest_framework import serializers
from sq_spec_portal_backend_core.models.code_implementation_trace_model import (
    CodeImplementationTraceModel,
)


class CodeImplementationTraceSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source="project.id", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    specification_id = serializers.IntegerField(
        source="specification.id", read_only=True
    )
    specification_name = serializers.CharField(
        source="specification.name", read_only=True
    )
    specification_revision_id = serializers.IntegerField(
        source="specification_revision.id", read_only=True
    )
    latest_version = serializers.CharField(
        source="specification_revision.version", read_only=True
    )

    class Meta:
        model = CodeImplementationTraceModel
        fields = "__all__"
