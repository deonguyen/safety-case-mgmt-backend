import django_filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from sq_spec_portal_backend_core.models import ProjectCodeBuildSnapshotTestSuiteModel
from sq_spec_portal_backend_snapshot.serializers.project_code_build_snapshot_test_suite_serializer import ProjectCodeBuildSnapshotTestSuiteSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class ProjectCodeBuildSnapshotTestSuiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Project Code Build Snapshot Test Suites to be viewed or edited.
    """
    queryset = ProjectCodeBuildSnapshotTestSuiteModel.objects.all()
    serializer_class = ProjectCodeBuildSnapshotTestSuiteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["project", "project_code_build_snapshot", "test_suite"]