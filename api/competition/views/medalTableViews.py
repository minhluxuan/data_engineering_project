from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import MedalTable
from ..serializers import MedalTableSerializer


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
