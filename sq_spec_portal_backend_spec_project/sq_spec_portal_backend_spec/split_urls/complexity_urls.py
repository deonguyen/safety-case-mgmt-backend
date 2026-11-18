from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.complexity_view import ComplexityViewSet

router = DefaultRouter()
router.register(r"complexities", ComplexityViewSet, basename="complexity")

urlpatterns = router.urls
