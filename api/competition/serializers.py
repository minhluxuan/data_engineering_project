from rest_framework import serializers
from .models import MedalTable


class MedalTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedalTable
        fields = '__all__'
