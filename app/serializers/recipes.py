from rest_framework import serializers

from models import MaterialList


class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialList
        fields = '__all__'