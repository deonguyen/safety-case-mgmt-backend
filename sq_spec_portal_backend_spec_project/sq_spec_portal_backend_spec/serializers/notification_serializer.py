from rest_framework import serializers
from sq_spec_portal_backend_core.models.notification_model import NotificationModel

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = ["id", "user", "title", "message", "is_read", "created_at"]
        read_only_fields = ["id", "user", "created_at"]