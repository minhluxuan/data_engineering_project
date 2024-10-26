from django.shortcuts import render
from django.db import connection
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
    # event_res = pd.read_csv("D:\CO3127_ProjectOlympics\data_engineering_project\data\processed\Olympic_Athlete_Event_Details_Processed.csv")
    # Loại bỏ các hàng trùng lặp
    event_res = event_res.drop_duplicates()
    # Tách thông tin medal ra khỏi event_res
    medal_res = event_res[['edition_id', 'country_noc',
                           'result_id', 'athlete_id', 'medal']].dropna(subset=['medal'])
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

# @api_view(['GET'])
# def check_connection(request):
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT 1;")
#             cursor.fetchone()
#         return Response({"message": "Database connection successful"}, status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({"message": f"Database connection failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventResultView(APIView):

    def post(self, request):
        try:
            body = request.data
            new_game_data, message, status_code = EventResultService.create(
                body)
            return Response({"message": message, "data": new_game_data}, status=status_code)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get(self, request, id1, id2, id3, id4):
    #     try:
    #         get_data, message, status_code = EventResultService.search(id1, id2, id3, id4)
    #         return Response(get_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, edition_id, country_noc, result_id, athlete_id):
        try:
            data = request.data  # Lấy dữ liệu từ request
            updated_data, message, status_code = EventResultService.update(
                edition_id, country_noc, result_id, athlete_id, data)
            return Response({
                'data': updated_data,
                'message': message
            }, status=status_code)
        except Exception as e:
            return Response({
                'data': None,
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, edition_id, country_noc, result_id, athlete_id):
        try:
            get_data, message, status_code = EventResultService.search(
                edition_id, country_noc, result_id, athlete_id)
            print(message)
            return Response(get_data, status=status_code)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, edition_id, country_noc, result_id, athlete_id):
        try:
            # Gọi service để thực hiện thao tác xóa
            response, message, status_code = EventResultService.delete(
                edition_id, country_noc, result_id, athlete_id)

            # Trả về kết quả nếu xóa thành công
            return Response({
                'message': message,
            }, status=status_code)

        except EventResult.DoesNotExist:
            # Trả về thông báo nếu không tìm thấy bản ghi
            return Response({
                'message': "Event result not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            # Trả về thông báo lỗi chi tiết
            return Response({
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
