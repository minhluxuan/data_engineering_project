import pandas as pd
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializers import ResultSerializer
from .services import ResultService
from rest_framework import status

# Create your views here.
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
            'result_countries': row['result_countries'],  # Nếu bạn có noc trong CSV
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