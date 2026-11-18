from rest_framework.routers import DefaultRouter
from sq_spec_portal_backend_spec.views.user_setting_view import UserSettingViewSet

router = DefaultRouter()
router.register(r"usersettings", UserSettingViewSet, basename="usersetting")

urlpatterns = router.urls