from django.shortcuts import render
from .serializers import MedalTableSerializer
from .models import MedalTable
import pandas as pd
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import ResultSerializer
from .services import ResultService
from rest_framework import status
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


@api_view(['POST'])
def upload_result(request):
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

    # Lặp qua từng dòng và lưu vào cơ sở dữ liệu
    for _, row in df.iterrows():
        game_data = {
            'result_id': row['result_id'],
            'event_title': row['event_title'],
            'sport': row['sport'],
            'sport_url': row['sport_url'],
            'result_location': row['result_location'],
            'result_participants': row['result_participants'],
            # Nếu bạn có noc trong CSV
            'result_countries': row['result_countries'],
            'start_date': row['start_date'],
            'end_date': row['end_date'],
            'result_format': row['result_format'],
            'result_detail': row['result_detail'],
            'result_description': row['result_description'],
            'edition_id': row['edition_id']
        }

        serializer = ResultSerializer(data=game_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Result uploaded successfully'}, status=status.HTTP_201_CREATED)


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
    def put(self, request, result_id, athlete_id):
        try:
            data = request.data  # Lấy dữ liệu từ request
            updated_data, message, status_code = EventResultService.update(
                result_id, athlete_id, data)
            return Response({
                'data': updated_data,
                'message': message
            }, status=status_code)
        except Exception as e:
            return Response({
                'data': None,
                'message': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, result_id, athlete_id):
        try:
            get_data, message, status_code = EventResultService.search(
                result_id, athlete_id)
            return Response(get_data, status=status_code)
        except Exception as e:
            print('----------------here exception----------------')
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, result_id, athlete_id):
        try:
            # Gọi service để thực hiện thao tác xóa
            response, message, status_code = EventResultService.delete(
                result_id, athlete_id)

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


class ResultView(APIView):
    def post(self, request):
        try:
            print('Heloo Niggga')
            body = request.data
            new_result_data, message, status_code = ResultService.create(body)
            return Response({"message": message, "data": new_result_data}, status=status_code)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({
                'data': None,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            results = ResultService.search()
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'data': None,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            data = request.data  # Lấy dữ liệu từ request
            updated_data, message, status_code = ResultService.update(id, data)
            return Response({
                'data': updated_data,
                'message': message
            }, status=status_code)
        except Exception as e:
            return Response({
                'data': None,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            _, message, status_code = ResultService.delete(id)
            return Response({
                'data': None,
                'message': message,
            }, status=status_code)
        except:
            return Response({
                'data': None,
                'message': 'An error occurs'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MedalTableView(APIView):
    def get(self, request):
        try:
            noc = request.query_params.get('noc')
            edition_id = request.query_params.get('edition_id')

            queryset = MedalTable.objects.all()

            if noc:
                queryset = queryset.filter(country_noc=noc)
            if edition_id:
                queryset = queryset.filter(edition_id=edition_id)

            # medal_tallies = MedalTable.objects.all()
            serializer = MedalTableSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get(self, request, id):
    #     try:
    #         medal_tally = MedalTable.objects.get(id=id)
    #         serializer = MedalTableSerializer(medal_tally)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except MedalTable.DoesNotExist:
    #         return Response({"message": "Medal tally not found"}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = MedalTableSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            medal_tally = MedalTable.objects.get(id=id)
            serializer = MedalTableSerializer(medal_tally, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MedalTable.DoesNotExist:
            return Response({"message": "Medal tally not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            medal_tally = MedalTable.objects.get(id=id)
            medal_tally.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MedalTable.DoesNotExist:
            return Response({"message": "Medal tally not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
