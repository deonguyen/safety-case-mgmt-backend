from sq_spec_portal_backend_core.models.specification_revision_model import SpecificationRevisionModel
from rest_framework import serializers


class SpecificationRevisionSerializer(serializers.ModelSerializer):
    specification_id = serializers.ReadOnlyField(source="specification.id")
    
    class Meta:
        model = SpecificationRevisionModel
        fields = "__all__"
