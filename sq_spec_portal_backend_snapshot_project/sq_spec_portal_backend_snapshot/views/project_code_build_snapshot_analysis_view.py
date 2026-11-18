import django_filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotAnalysisModel
from sq_spec_portal_backend_snapshot.serializers.project_code_build_snapshot_analysis_serializer import ProjectCodeBuildSnapshotAnalysisSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class ProjectCodeBuildSnapshotAnalysisViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Project Code Build Snapshot Analyses to be viewed or edited.
    """
    queryset = ProjectCodeBuildSnapshotAnalysisModel.objects.all()
    serializer_class = ProjectCodeBuildSnapshotAnalysisSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["project", "project_code_build_snapshot"]