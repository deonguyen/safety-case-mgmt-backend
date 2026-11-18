from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_snapshot.views.project_code_build_snapshot_analysis_view import \
    ProjectCodeBuildSnapshotAnalysisViewSet

router = DefaultRouter()
router.register(r"project-code-build-snapshot-analyses", ProjectCodeBuildSnapshotAnalysisViewSet, basename="projectcodebuildsnapshotanalysis")

urlpatterns = [
    path("", include(router.urls)),
]