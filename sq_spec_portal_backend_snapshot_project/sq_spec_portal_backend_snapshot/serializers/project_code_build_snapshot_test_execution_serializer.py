from rest_framework import serializers
from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotTestExecutionModel


class ProjectCodeBuildSnapshotTestExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCodeBuildSnapshotTestExecutionModel
        fields = '__all__'