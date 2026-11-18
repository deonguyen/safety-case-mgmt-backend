from rest_framework import serializers
from sq_spec_portal_backend_core.models.code_implementation_trace_log_model import (
    CodeImplementationTraceLogModel,
)


class CodeImplementationTraceLogSerializer(serializers.ModelSerializer):
    code_implementation_trace_id = serializers.IntegerField(
        source="code_implementation_trace.id", read_only=True
    )
    project_id = serializers.IntegerField(source="project.id", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    specification_name = serializers.CharField(
        source="specification.name", read_only=True
    )
    trace_id = serializers.CharField(
        source="code_implementation_trace.id", read_only=True
    )
    trace_type = serializers.CharField(
        source="code_implementation_trace.type", read_only=True
    )

    class Meta:
        model = CodeImplementationTraceLogModel
        fields = "__all__"
