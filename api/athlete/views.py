from django.shortcuts import render

import pandas as pd
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import AthleteBioSerializer
from .services import AthleteBioService
from rest_framework import status
from .models import Athlete_Bio


@api_view(['POST'])
def uploadFile(request):
    print(request.FILES)

    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']

    df = pd.read_csv(file, chunksize=1000)

    for chunk in df:
        for _, row in chunk.iterrows():
            data = {
                'athlete_id': row['athlete_id'],
                'name': row['name'],
                'sex': row['sex'],
                'born': row['born'],
                'height': row['height'],
                'weight': row['weight'],
                'country_noc': row['country_noc'],
                'description': row['description'],
                'special_notes': row['special_notes'],
                'country': row['country']
            }
            print(data)
            athlete_data, message, status_code = AthleteBioService.create(data)
            if status_code != 201:
                return Response(message, status=status_code)

    return Response({"message": "Create sucessful"}, status=200)


class AthleteBioView(APIView):
    def post(self, request):
        try:
            data = request.data
            new_athlete, message, status_code = AthleteBioService.create(data)
            return Response({"data": new_athlete, "message": message}, status=status_code)
        except Exception as e:
            return Response(f"Error occurr is {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, id=None):
        try:
            # id = request.query_params.get('id')
            print("here")
            if id:
                athlete, message, status_code = AthleteBioService.searchById(
                    id)
                print(message)
                return Response(data=athlete, status=status_code)
            else:
                athletes = AthleteBioService.search()
                return Response(data=athletes, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(f"Error occurr is {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            data, message, status_code = AthleteBioService.update(
                id, request.data)
            print("-------------------", status_code)
            return Response({"message": message, "data": data}, status=status_code)

        except Exception as e:
            return Response(f"Error occurr is {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            _, message, status_code = AthleteBioService.delete(id)
            return Response(data={"message": message}, status=status_code)

        except Exception as e:
            return Response(f"Error occurr is {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
