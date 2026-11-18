from rest_framework import permissions, viewsets

from sq_spec_portal_backend_core.models.test_execution_trace_model import TestExecutionTraceModel
from sq_spec_portal_backend_spec.serializers.test_execution_trace_serializer import (
    TestExecutionTraceSerializer,
)


class TestExecutionTraceViewSet(viewsets.ModelViewSet):
    queryset = TestExecutionTraceModel.objects.all().order_by("-id")
    serializer_class = TestExecutionTraceSerializer
    permission_classes = [permissions.IsAuthenticated]