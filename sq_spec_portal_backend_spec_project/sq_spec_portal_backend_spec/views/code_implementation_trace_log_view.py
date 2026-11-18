from rest_framework.decorators import action
import django_filters
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from sq_spec_portal_backend_core.models.code_implementation_trace_log_model import (
    CodeImplementationTraceLogModel,
)
from sq_spec_portal_backend_spec.serializers.code_implementation_trace_log_serializer import (
    CodeImplementationTraceLogSerializer,
)
from sq_spec_portal_backend_core.models.code_implementation_trace_model import (
    CodeImplementationTraceModel,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = None
    page_size_query_param = "page_size"
    max_page_size = None


class CodeImplementationTraceLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Code Implementation Trace Logs to be viewed or edited.
    """

    queryset = CodeImplementationTraceLogModel.objects.all().order_by("-id")
    serializer_class = CodeImplementationTraceLogSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["project", "code_implementation_trace"]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            project_id = request.query_params.get("project_id")
            trace_type = request.query_params.get("trace_type")
            specification_name = request.query_params.get("specification_name")

            if project_id:
                queryset = queryset.filter(project_id=project_id)
            if trace_type:
                queryset = queryset.filter(code_implementation_trace__type=trace_type)
            if specification_name:
                queryset = queryset.filter(
                    code_implementation_trace__specification__name__icontains=specification_name
                )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data

            for item in data:
                trace_id = item.get("code_implementation_trace")
                if isinstance(trace_id, dict):
                    trace_id = trace_id.get("id")
                trace = CodeImplementationTraceModel.objects.filter(id=trace_id).first()
                item["specification_name"] = (
                    trace.specification.name
                    if trace and getattr(trace, "specification", None)
                    else None
                )

            if page is not None:
                return self.get_paginated_response(data)

            return Response(data)
        except Exception as e:
            return f"Error: {e}"
    
    @action(detail=False, methods=["get"])
    def get_specification_implement_count(self, request):
        """
        Custom action to get distinct specification type using a raw SQL query.
        """

        project_id = request.query_params.get("project_id")
        if not project_id:
            return Response(
                {"error": "The 'project_id' parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            from django.db import connection
            import os

            sql_file_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "sql_queries",
                "select_specification_implement_count.sql",
            )
            with open(sql_file_path, "r", encoding="utf-8") as f:
                sql_query = f.read()
            
            with connection.cursor() as cursor:
                cursor.execute(sql_query, [project_id])
                results = cursor.fetchall()

            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    