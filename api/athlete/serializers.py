from .models import Athlete_Bio
from rest_framework import serializers

class AthleteBioSerializer(serializers.ModelSerializer):

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
      'special_notes', 
      'country'
  ]