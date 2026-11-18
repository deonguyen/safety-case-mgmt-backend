from sq_spec_portal_backend_spec.views.github_view import GitHubViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"github", GitHubViewSet, basename="github")
urlpatterns = router.urls
