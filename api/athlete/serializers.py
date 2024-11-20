from .models import Athlete_Bio
from rest_framework import serializers

class AthleteBioSerializer(serializers.ModelSerializer):
  athlete_id = serializers.IntegerField(read_only=True)
  born = serializers.CharField(allow_null=True, required=False)
  description = serializers.CharField(allow_null=True, required=False)
  special_notes = serializers.CharField(allow_null=True, required=False)
  class Meta:
    model = Athlete_Bio
    fields = [
      'athlete_id', 
      'name', 
      'sex', 
      'born', 
      'height', 
      'weight', 
      'country_noc', 
      'description', 
      'special_notes'
  ]