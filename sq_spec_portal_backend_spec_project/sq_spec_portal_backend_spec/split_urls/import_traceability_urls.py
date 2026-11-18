from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.import_traceability_view import ImportTraceabilityViewSet

router = DefaultRouter()
router.register(r"import-traceability", ImportTraceabilityViewSet, basename="importtraceability")

urlpatterns = [
    path(
        "import-traceability/import_traceability_from_repos_code_search/",
        ImportTraceabilityViewSet.as_view({"post": "import_traceability_from_repos_code_search"}),
        name="import-traceability-from-repos-code-search",
    ),
    path(
        "import-traceability/import_traceability_from_repos_pr_search/",
        ImportTraceabilityViewSet.as_view({"post": "import_traceability_from_repos_pr_search"}),
        name="import-traceability-from-repos-pr-search",
    ),
    path(
        "import-traceability/import_traceability_for_repos/",
        ImportTraceabilityViewSet.as_view({"post": "import_traceability_for_repos"}),
        name="import-traceability-for-repos",
    ),
    path("", include(router.urls)),
]
