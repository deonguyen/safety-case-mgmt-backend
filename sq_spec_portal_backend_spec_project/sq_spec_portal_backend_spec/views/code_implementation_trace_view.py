import os
from django.conf import settings
import django_filters
from docx import Document
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from sq_spec_portal_backend_core.models import CodeImplementationTraceModel
from sq_spec_portal_backend_spec.serializers.code_implementation_trace_serializer import (
    CodeImplementationTraceSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = "page_size"
    max_page_size = None


class CodeImplementationTraceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Code Implementation Traces to be viewed or edited.
    """

    queryset = CodeImplementationTraceModel.objects.all().order_by("-id")
    serializer_class = CodeImplementationTraceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["project"]

    @action(detail=False, methods=["get"])
    def get_code_dependency_traces(self, request, *args, **kwargs):
        """
        Custom action to retrieve code dependency traces for a specific project.
        """
        # Resolve the path to results.docx
        file_path = os.path.join(getattr(settings, "BASE_DIR", ""), "results.docx")
        if not os.path.exists(file_path):
            # Fallback to local execution path
            file_path = "results.docx"
            if not os.path.exists(file_path):
                return Response(
                    {"error": "results.docx file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        mermaid_lines = ["graph TD"]

        try:
            document = Document(file_path)

            for table in document.tables:
                for row in table.rows:
                    cells = row.cells
                    # Ensure row has at least 4 columns (index 3 is the 4th column)
                    if len(cells) >= 4:
                        target = cells[3].text.strip()

                        if target:
                            mermaid_lines.append(f"{target}")

            return Response(
                {"diagram": "\n".join(mermaid_lines)}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
