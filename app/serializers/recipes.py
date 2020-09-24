from rest_framework import serializers

from app.models import MaterialList


class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialList
        fields = '__all__'