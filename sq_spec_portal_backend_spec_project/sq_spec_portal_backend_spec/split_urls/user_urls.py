from django.urls import include, path
from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.user_view import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
