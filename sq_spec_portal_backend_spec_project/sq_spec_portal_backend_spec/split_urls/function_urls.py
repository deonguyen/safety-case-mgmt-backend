from sq_spec_portal_backend_spec.views.function_view import FunctionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"functions", FunctionViewSet)
urlpatterns = router.urls
