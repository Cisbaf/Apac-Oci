from rest_framework import serializers
from .models import EstablishmentModel


class EstablishmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentModel
        fields = '__all__'

    def to_representation(self, instance):
        return instance.to_entity().model_dump()