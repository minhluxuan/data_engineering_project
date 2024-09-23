from rest_framework import serializers
from .models import Game, Country

class CountryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'  # Hoặc chỉ định các trường cụ thể
