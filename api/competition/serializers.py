from .models import EventResult, MedalResult
from rest_framework import serializers
from .models import MedalTable


class MedalTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedalTable
        fields = '__all__'


class EventResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventResult
        fields = '__all__'


class MedalResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedalResult
        fields = '__all__'  # Hoặc chỉ định các trường cụ thể
