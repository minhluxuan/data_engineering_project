import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Result
from .serializers import ResultSerializer


class ResultService:
    def __init__(self):
        pass

    @staticmethod
    def create(data):
        print("I'm hear")
        try:
            serializer = ResultSerializer(data=data)
            print("WTF")
            if serializer.is_valid():
                print("Valid")
                serializer.save()
                return serializer.data, "Created successfully", status.HTTP_201_CREATED
            else:
                print("Invalid")
                # Print or log detailed errors for each field
                for field, errors in serializer.errors.items():
                    print(f"Field '{field}' has errors: {errors}") 
                return None, serializer.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return None, f"An error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @staticmethod
    def search():
        results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        return serializer.data
    
    @staticmethod
    @staticmethod
    def update(edition_id, data):
        try:
            
            result = Result.objects.get(edition_id=edition_id)
            serializer = ResultSerializer(result, data=data)
            
            # Kiểm tra tính hợp lệ của dữ liệu
            if serializer.is_valid():
                serializer.save()
                return serializer.data, "Update succesfully", status.HTTP_200_OK
            else:
                return None, serializer.errors, status.HTTP_400_BAD_REQUEST
        except Result.DoesNotExist:
            return None, "Result not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return None, "An error occurs", status.HTTP_500_INTERNAL_SERVER_ERROR
        
    @staticmethod
    def delete(id):
        try:
            result = Result.objects.get(edition_id=id)

            if not result:
                return None, "Result does not exist", status.HTTP_404_NOT_FOUND
            
            result.delete()
            return None, "Result deleted successfully", status.HTTP_200_OK
        except Result.DoesNotExist:
            return None, "Result not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return None, "An error occurs", status.HTTP_500_INTERNAL_SERVER_ERROR
        