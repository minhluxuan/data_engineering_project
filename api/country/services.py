import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Country, Game
from .serializers import CountryProfileSerializer, GameSerializer


class CountryService:
    def __init__(self):
        pass
    
    @staticmethod
    def search():
        countries = Country.objects.all()
        serializer = CountryProfileSerializer(countries, many=True)
        return serializer.data
    
class GameService:
    def __init__(self):
        pass

    @staticmethod
    def search():
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return serializer.data
    
    @staticmethod
    def update(edition_id, data):
        try:
            # Tìm game theo ID
            game = Game.objects.get(edition_id=edition_id)
            serializer = GameSerializer(game, data=data)
            
            # Kiểm tra tính hợp lệ của dữ liệu
            if serializer.is_valid():
                serializer.save()  # Lưu game đã cập nhật
                return serializer.data, "Update succesfully", status.HTTP_200_OK
            else:
                return None, serializer.errors, status.HTTP_400_BAD_REQUEST
        except Game.DoesNotExist:
            return None, "Game not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return None, "An error occurs", status.HTTP_500_INTERNAL_SERVER_ERROR
        
    @staticmethod
    def create(data):
        try:
            serializer = GameSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return serializer.data, "Created successfully", status.HTTP_201_CREATED
            else:
                return None, serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return None, f"An error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR
