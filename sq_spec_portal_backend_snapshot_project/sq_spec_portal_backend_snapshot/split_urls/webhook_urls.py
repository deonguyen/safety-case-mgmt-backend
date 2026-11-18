from django.urls import path
from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_snapshot.views.webhook_view import WebhookViewSet

router = DefaultRouter()
router.register(r"vertexai", WebhookViewSet, basename="webhook")

urlpatterns = [
    path(
        "github_webhook/",
        WebhookViewSet.as_view({"post": "github_webhook"}),
        name="webhook-github",
    ),
] + router.urls
