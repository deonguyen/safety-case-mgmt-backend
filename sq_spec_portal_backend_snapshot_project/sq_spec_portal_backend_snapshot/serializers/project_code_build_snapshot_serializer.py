from rest_framework import serializers
from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotModel


class ProjectCodeBuildSnapshotSerializer(serializers.ModelSerializer):
    project_id = serializers.ReadOnlyField(source="project.id")

    class Meta:
        model = ProjectCodeBuildSnapshotModel
        fields = "__all__"
