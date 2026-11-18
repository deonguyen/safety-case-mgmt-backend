from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_snapshot.views.project_code_build_snapshot_test_execution_view import \
    ProjectCodeBuildSnapshotTestExecutionViewSet

router = DefaultRouter()
router.register(r"project-code-build-snapshot-test-executions", ProjectCodeBuildSnapshotTestExecutionViewSet, basename="projectcodebuildsnapshottestexecution")

urlpatterns = [
    path("", include(router.urls)),
]