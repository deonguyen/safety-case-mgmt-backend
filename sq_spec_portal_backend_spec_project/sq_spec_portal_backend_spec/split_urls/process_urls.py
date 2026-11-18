from sq_spec_portal_backend_spec.views.github_view import GitHubViewSet
from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.process_view import ProcessViewSet

router = DefaultRouter()
router.register(r"process", ProcessViewSet)
urlpatterns = router.urls
