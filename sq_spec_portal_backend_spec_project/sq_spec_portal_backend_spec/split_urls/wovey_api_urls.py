from sq_spec_portal_backend_spec.views.wovey_api_view import WoveyAPIViewSet
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"vertexai", WoveyAPIViewSet, basename="woveyapi")

# urlpatterns = [
#     path(
#         "woveyapi/diffsummary/",
#         WoveyAPIViewSet.as_view({"post": "diffsummary"}),
#         name="woveyapi-diffsummary",
#     ),
# ] + router.urls
