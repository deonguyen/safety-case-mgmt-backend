from rest_framework import serializers
from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotSpecificationModel


class ProjectCodeBuildSnapshotSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCodeBuildSnapshotSpecificationModel
        fields = '__all__'