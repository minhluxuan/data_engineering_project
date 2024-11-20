from .models import Result
from .models import EventResult, MedalResult
from rest_framework import serializers
from .models import MedalTable


class MedalTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedalTable
        fields = '__all__'


class EventResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pos = serializers.CharField(allow_null=True, required=False)
    class Meta:
        model = EventResult
        fields = '__all__'


class MedalResultSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = MedalResult
        fields = '__all__'  # Hoặc chỉ định các trường cụ thể


class ResultSerializer(serializers.ModelSerializer):
    result_id = serializers.IntegerField(read_only=True)
    sport_url = serializers.CharField(allow_null=True, required=False)
    result_location = serializers.CharField(allow_null=True, required=False)
    result_format = serializers.CharField(allow_null=True, required=False)
    result_detail = serializers.CharField(allow_null=True, required=False)
    result_description = serializers.CharField(allow_null=True, required=False)
    
    class Meta:
        model = Result
        fields = '__all__'
