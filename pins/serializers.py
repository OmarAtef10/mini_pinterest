from rest_framework import serializers

from pins.models import Pin


class PinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pin
        fields = '__all__'