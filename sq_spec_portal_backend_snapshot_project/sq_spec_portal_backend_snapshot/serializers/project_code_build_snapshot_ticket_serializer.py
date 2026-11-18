from rest_framework import serializers
from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotTicketModel


class ProjectCodeBuildSnapshotTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCodeBuildSnapshotTicketModel
        fields = '__all__'