from django.urls import path
from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.specification_view import SpecificationViewSet

router = DefaultRouter()
router.register(r"specifications", SpecificationViewSet)

urlpatterns = [
    path(
        "specifications/get_specification_by_sql/",
        SpecificationViewSet.as_view({"get": "get_specification_by_sql"}),
        name="get-specification-by-sql",
    ),
    path(
        "specifications/get_jama_specification_hierarchy/",
        SpecificationViewSet.as_view({"get": "get_jama_specification_hierarchy"}),
        name="get-jama-specification-hierarchy",
    ),
    path(
        "specifications/get_distinct_specification_type/",
        SpecificationViewSet.as_view({"get": "get_distinct_specification_type"}),
        name="get-distinct-specification-type",
    ),
] + router.urls
