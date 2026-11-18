from django.urls import include, path
from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.specification_test_case_view import SpecificationTestCaseViewSet

router = DefaultRouter()
router.register(r"specification-test-cases", SpecificationTestCaseViewSet, basename="specificationtestcase")

urlpatterns = [
    path("", include(router.urls)),
]
