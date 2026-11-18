from django.urls import path, include
from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_spec.views.code_implementation_trace_log_view import (
    CodeImplementationTraceLogViewSet,
)

router = DefaultRouter()
router.register(
    r"code-implementation-trace-logs",
    CodeImplementationTraceLogViewSet,
    basename="code-implementation-trace-log",
)

urlpatterns = [
    path(
        "code-implementation-trace-logs/get_specification_implement_count/",
        CodeImplementationTraceLogViewSet.as_view(
            {"get": "get_specification_implement_count"}
        ),
        name="get-specification-implement-count",
    ),
    path("", include(router.urls)),
]
