from django.shortcuts import render

import pandas as pd
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import CountryProfileSerializer, GameSerializer
from country.services import CountryService, GameService
from rest_framework import status


@api_view(['POST'])
def upload_games(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    # print(file)
    # if not file.name.endswith('.csv'):
    #     return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)

    # Đọc dữ liệu từ file CSV vào DataFrame
    df = pd.read_csv(file)

    def parse_date(date_str):
        if pd.isna(date_str) or date_str == 'None':
            return None  # hoặc bạn có thể cung cấp một giá trị mặc định
        try:
            # Chuyển đổi ngày về định dạng YYYY-MM-DD
            return pd.to_datetime(date_str, errors='coerce').strftime('%Y-%m-%d')
        except Exception:
            return None

    # Áp dụng hàm chuyển đổi ngày cho các cột
    df['start_date'] = df['start_date'].apply(parse_date)
    df['end_date'] = df['end_date'].apply(parse_date)
    df['competition_start_date'] = df['competition_start_date'].apply(
        parse_date)
    df['competition_end_date'] = df['competition_end_date'].apply(parse_date)

    # Lặp qua từng dòng và lưu vào cơ sở dữ liệu
    for _, row in df.iterrows():
        game_data = {
            'edition': row['edition'],
            'edition_id': row['edition_id'],
            'edition_url': row['edition_url'],
            'year': row['year'],
            'city': row['city'],
            'country_flag_url': row['country_flag_url'],
            'country_noc': row['country_noc'],  # Nếu bạn có noc trong CSV
            'start_date': row['start_date'],
            'end_date': row['end_date'],
            'is_held': row['isHeld'],
            'competition_start_date': row['competition_start_date'],
            'competition_end_date': row['competition_end_date'],
        }

        serializer = GameSerializer(data=game_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Games uploaded successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def upload_country_profiles(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    # Kiểm tra định dạng file có phải là CSV không
    # if not file.name.endswith('.csv'):
    #     return Response({'error': 'File is not CSV type'}, status=status.HTTP_400_BAD_REQUEST)

    # Đọc dữ liệu từ file CSV vào DataFrame
    df = pd.read_csv(file)

    # Kiểm tra xem các cột cần thiết có tồn tại không
    if 'noc' not in df.columns or 'country' not in df.columns:
        return Response({'error': 'File does not contain required columns (noc, country)'}, status=status.HTTP_400_BAD_REQUEST)

    # Lặp qua từng dòng và lưu vào cơ sở dữ liệu
    for _, row in df.iterrows():
        country_profile_data = {
            'noc': row['noc'],
            'country': row['country'],
        }

        serializer = CountryProfileSerializer(data=country_profile_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Country profiles uploaded successfully'}, status=status.HTTP_201_CREATED)


class CountryView(APIView):
    def get(self, requests):
        try:
            countries = CountryService.search()
            return Response(countries, status=status.HTTP_200_OK)
        except:
            return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GameView(APIView):
    def post(self, request):
        try:
            body = request.data
            new_game_data, message, status_code = GameService.create(body)
            return Response({"message": message, "data": new_game_data}, status=status_code)

        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            games = GameService.search()
            return Response(games, status=status.HTTP_200_OK)
        except:
            return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            data = request.data  # Lấy dữ liệu từ request
            updated_data, message, status_code = GameService.update(id, data)
            return Response({
                'data': updated_data,
                'message': message
            }, status=status_code)
        except:
            return Response({
                'data': None,
                'message': 'An error occurs'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            _, message, status_code = GameService.delete(id)
            return Response({
                'data': None,
                'message': message,
            }, status=status_code)
        except:
            return Response({
                'data': None,
                'message': 'An error occurs'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            _, message, status_code = GameService.delete(id)
            return Response({
                'data': None,
                'message': message,
            }, status=status_code)
        except:
            return Response({
                'data': None,
                'message': 'An error occurs'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
