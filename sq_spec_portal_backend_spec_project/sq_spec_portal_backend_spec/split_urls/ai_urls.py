from django.urls import path
from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_spec.views.ai_view import AIViewSet


router = DefaultRouter()
router.register(r"ai", AIViewSet, basename="ai")

urlpatterns = [
    path("ai/generatediagram/", AIViewSet.as_view({"post": "generatediagram"}), name="ai-generatediagram"),
    path("ai/generatetestcases/", AIViewSet.as_view({"post": "generatetestcases"}), name="ai-generatetestcases"),
    path("ai/diffsummary/", AIViewSet.as_view({"post": "diffsummary"}), name="ai-diffsummary"),
] + router.urls
