from sq_spec_portal_backend_spec.views.project_specification_view import ProjectSpecificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"project-specifications", ProjectSpecificationViewSet)
urlpatterns = router.urls
