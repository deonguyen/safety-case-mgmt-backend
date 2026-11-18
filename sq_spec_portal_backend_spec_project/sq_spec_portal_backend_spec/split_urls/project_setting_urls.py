from rest_framework.routers import DefaultRouter

from sq_spec_portal_backend_spec.views.project_setting_view import ProjectSettingViewSet


router = DefaultRouter()
router.register(r"project-settings", ProjectSettingViewSet, basename="project-setting")

urlpatterns = router.urls