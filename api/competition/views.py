from django.shortcuts import render

import pandas as pd
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import EventResult, MedalResult
from .serializers import EventResultSerializer, MedalResultSerializer
from competition.services import EventResultService
from rest_framework import status

@api_view(['POST'])
def upload_event_results(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    file = request.FILES['file']
    # Đọc file CSV
    event_res = pd.read_csv(file)
    # Loại bỏ các hàng trùng lặp
    event_res = event_res.drop_duplicates()
    # Tách thông tin medal ra khỏi event_res
    medal_res = event_res[['edition_id', 'country_noc', 'result_id', 'athlete_id', 'medal']].dropna(subset=['medal'])
    # Loại bỏ cột 'medal' khỏi event_res
    event_res = event_res.drop(columns=['medal'])
    # Lưu event_res
    for _, row in event_res.iterrows():
        event_result_data = {
            'edition_id': row['edition_id'],
            'country_noc': row['country_noc'],
            'sport': row['sport'], 
            'event': row['event'],
            'result_id': row['result_id'],
            'athlete_id': row['athlete_id'],
            'pos': row['pos'],
            'isTeamSport': row['isTeamSport'],
        }
        event_serializer = EventResultSerializer(data=event_result_data)
        if event_serializer.is_valid():
            event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Lưu medal_res
    for _, row in medal_res.iterrows():
        medal_result_data = {
            'edition_id': row['edition_id'],
            'country_noc': row['country_noc'],
            'result_id': row['result_id'],
            'athlete_id': row['athlete_id'],
            'medal': row['medal'],
        }
        medal_serializer = MedalResultSerializer(data=medal_result_data)
        if medal_serializer.is_valid():
            medal_serializer.save()
        else:
            return Response(medal_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Event and Medal results uploaded successfully'}, status=status.HTTP_201_CREATED)

class EventResultView(APIView):
    
    def post(self, request):
        try:
            body = request.data
            new_game_data, message, status_code = EventResultService.create(body)
            return Response({"message": message, "data": new_game_data}, status=status_code)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            games = EventResultService.search()
            return Response(games, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, athlete_id, result_id, country_noc, edition_id):
        try:
            data = request.data  # Lấy dữ liệu từ request
            updated_data, message, status_code = EventResultService.update(athlete_id, result_id, country_noc, edition_id, data)
            return Response({
                'data': updated_data,
                'message': message
            }, status=status_code)
        except Exception as e:
            return Response({
                'data': None,
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, athlete_id, result_id, country_noc, edition_id):
        try:
            _, message, status_code = EventResultService.delete(athlete_id, result_id, country_noc, edition_id)
            return Response({
                'data': None,
                'message': message,
            }, status=status_code)
        except:
            return Response({
                'data': None,
                'message': 'An error occurs'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
