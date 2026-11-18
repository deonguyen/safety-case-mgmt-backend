from rest_framework import serializers
from sq_spec_portal_backend_core.models.process_model import ProcessModel


class ProcessSerializer(serializers.ModelSerializer):
    """Serializer for the Process model."""

    project_id = serializers.ReadOnlyField(source="project.id")
    project_name = serializers.ReadOnlyField(source="project.name")

    class Meta:
        model = ProcessModel
        fields = "__all__"
