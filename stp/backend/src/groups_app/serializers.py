from groups_app.models import Group
from rest_framework import serializers


class GroupOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = []
