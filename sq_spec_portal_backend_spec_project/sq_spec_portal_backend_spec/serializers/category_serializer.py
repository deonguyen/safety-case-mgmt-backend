from rest_framework import serializers

from sq_spec_portal_backend_core.models.category_model import CategoryModel

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"