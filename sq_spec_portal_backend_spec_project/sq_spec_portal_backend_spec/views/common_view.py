# Domain-specific logic shared across multiple sub-features.
class CommonViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def get_distinct_specification_type(self, request, *args, **kwargs):
        return None