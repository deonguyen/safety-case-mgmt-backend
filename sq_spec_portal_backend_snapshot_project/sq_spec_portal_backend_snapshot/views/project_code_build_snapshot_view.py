import django_filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotModel
from sq_spec_portal_backend_snapshot.serializers.project_code_build_snapshot_serializer import ProjectCodeBuildSnapshotSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class ProjectCodeBuildSnapshotViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Project Code Build Snapshots to be viewed or edited.
    """
    queryset = ProjectCodeBuildSnapshotModel.objects.all()
    serializer_class = ProjectCodeBuildSnapshotSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["build_status", "deploy_status", "github_event", "github_sha", "project", "workflow_run_id"]