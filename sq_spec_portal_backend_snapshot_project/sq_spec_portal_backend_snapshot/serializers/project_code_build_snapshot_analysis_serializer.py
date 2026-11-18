from rest_framework import serializers
from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotAnalysisModel


class ProjectCodeBuildSnapshotAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCodeBuildSnapshotAnalysisModel
        fields = '__all__'