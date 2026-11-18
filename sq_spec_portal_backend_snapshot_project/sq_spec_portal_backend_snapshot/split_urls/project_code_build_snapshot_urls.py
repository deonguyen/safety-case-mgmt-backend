from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_snapshot.views.project_code_build_snapshot_view import \
    ProjectCodeBuildSnapshotViewSet

router = DefaultRouter()
router.register(r"project-code-build-snapshots", ProjectCodeBuildSnapshotViewSet, basename="projectcodebuildsnapshot")

urlpatterns = [
    path("", include(router.urls)),
]