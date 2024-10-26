import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Athlete_Bio
from .serializers import AthleteBioSerializer

class AthleteBioService:
  def __init__(self):
    pass

  @staticmethod
  def create(data):
    try:
      serializer = AthleteBioSerializer(data = data)

      if serializer.is_valid():
        serializer.save()
        return serializer.data, "Created successfully", status.HTTP_201_CREATED
      else:
        return None, serializer.errors, status.HTTP_400_BAD_REQUEST
    except Exception as e:
      return None, f"An error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR

  @staticmethod
  def searchById(id):
    try:
        # Try to retrieve the athlete with the given id
        athlete = Athlete_Bio.objects.get(athlete_id=id)
        
        # Serialize the athlete object
        serializer = AthleteBioSerializer(athlete)
        
        # If data is valid, return the serialized data
        return serializer.data, "Get athlete successfully", status.HTTP_200_OK
    
    
    except Exception as e:
        if (str(e) == "Athlete_Bio matching query does not exist."):
          return None, f"Athlete have id {id} matching query does not exist.", status.HTTP_404_NOT_FOUND
      
        # Catch any other exceptions
        return None, f"An error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR

  @staticmethod
  def search():
    athletes = Athlete_Bio.objects.defer('id')[:20]

    serializer = AthleteBioSerializer(athletes, many=True)
    return serializer.data

  @staticmethod
  def update(athelet_id, data):
    try:
      athlete = Athlete_Bio.objects.get(athlete_id = athelet_id)     
      serializer = AthleteBioSerializer(athlete, data = data)
      print(data)
      
      if serializer.is_valid():
        serializer.save()
        return serializer.data, "Updated successfully", status.HTTP_200_OK
      else: 
        return None, serializer.errors, status.HTTP_400_BAD_REQUEST
    except Athlete_Bio.DoesNotExist:
        return None, "Athlete_id does not exist", status.HTTP_404_NOT_FOUND

    except Exception as e:
      print(e)
      return None, f"An error occurs {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR
    
  @staticmethod
  def delete(id):
    try:
      athlete = Athlete_Bio.objects.get(athlete_id = id)

      if not athlete:
        return None, f"Athlete {id} does not exist", status.HTTP_404_NOT_FOUND
      
      athlete.delete()
      return None, f"Delete athlete {id} successfully", status.HTTP_200_OK
    
    except Exception as e:
      return f"An error occurs {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR
