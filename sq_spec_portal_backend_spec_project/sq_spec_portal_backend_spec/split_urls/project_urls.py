from sq_spec_portal_backend_spec.views.project_view import ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
urlpatterns = router.urls
