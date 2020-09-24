from rest_framework import serializers

from app.models import ProductionOrder


class ProductionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionOrder
        fields = '__all__'