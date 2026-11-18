from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_snapshot.views.project_code_build_snapshot_test_suite_view import \
    ProjectCodeBuildSnapshotTestSuiteViewSet

router = DefaultRouter()
router.register(r"project-code-build-snapshot-test-suites", ProjectCodeBuildSnapshotTestSuiteViewSet, basename="projectcodebuildsnapshottestsuite")

urlpatterns = [
    path("", include(router.urls)),
]