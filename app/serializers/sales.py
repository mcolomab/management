from rest_framework import serializers

from .models import Sale, SaleDetail


class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ['product_id', 'quantity', 'unit_price', 'discount']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleDetailSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'