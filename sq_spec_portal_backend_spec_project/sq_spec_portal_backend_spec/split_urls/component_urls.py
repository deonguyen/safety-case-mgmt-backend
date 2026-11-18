from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_spec.views.component_view import ComponentViewSet

router = DefaultRouter()
router.register(r"components", ComponentViewSet)
urlpatterns = router.urls
