from rest_framework import serializers

from app.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'