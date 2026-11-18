from django.urls import path
from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.vertex_ai_view import VertexAIViewSet

router = DefaultRouter()
router.register(r"vertexai", VertexAIViewSet, basename="vertexai")

# urlpatterns = [
#     path("vertexai/generatediagram/", VertexAIViewSet.as_view({"post": "generatediagram"}), name="vertexai-generatediagram"),
#     path("vertexai/generatetestcases/", VertexAIViewSet.as_view({"post": "generatetestcases"}), name="vertexai-generatetestcases"),
#     path("vertexai/diffsummary/", VertexAIViewSet.as_view({"post": "diffsummary"}), name="vertexai-diffsummary"),
# ] + router.urls