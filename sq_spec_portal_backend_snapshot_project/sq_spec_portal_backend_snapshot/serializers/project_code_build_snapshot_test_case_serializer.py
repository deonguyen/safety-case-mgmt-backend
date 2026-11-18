from rest_framework import serializers
from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotTestCaseModel


class ProjectCodeBuildSnapshotTestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCodeBuildSnapshotTestCaseModel
        fields = '__all__'