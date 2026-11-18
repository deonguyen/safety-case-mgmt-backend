from rest_framework import serializers
from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotTestSuiteModel


class ProjectCodeBuildSnapshotTestSuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCodeBuildSnapshotTestSuiteModel
        fields = '__all__'