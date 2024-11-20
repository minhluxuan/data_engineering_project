import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Athlete_Bio
from .serializers import AthleteBioSerializer
import mysql.connector
import csv

# Connect to the database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='nhannt',
    database='do_an'
)

def height_process(country_noc_id, sex):
    cursor = conn.cursor()
    height_query = "SELECT AVG(height) FROM athlete_athlete_bio WHERE country_noc_id = %s AND sex = %s"
    cursor.execute(height_query, (country_noc_id, sex))
    height = cursor.fetchone()[0]
    return height if height else 0.0

def weight_process(country_noc_id, sex):
    cursor = conn.cursor()
    weight_query = "SELECT AVG(weight) FROM athlete_athlete_bio WHERE country_noc_id = %s AND sex = %s"
    cursor.execute(weight_query, (country_noc_id, sex))
    weight = cursor.fetchone()[0]
    return weight if weight else 0.0


class AthleteBioService:
    def __init__(self):
        pass

    @staticmethod
    def create(data):
        try:
            print(data)
            # Làm sạch dữ liệu đầu vào
            cleaned_data = {
                key: value[0] if isinstance(value, list) else value
                for key, value in data.items()
            }
            print(cleaned_data)
            # Chuyển đổi và kiểm tra dữ liệu
            try:
                if cleaned_data['height'] == '0':
                    cleaned_data['height'] = height_process(cleaned_data['country_noc'], cleaned_data['sex'])
                if cleaned_data['weight'] == '0':
                    cleaned_data['weight'] = weight_process(cleaned_data['country_noc'], cleaned_data['sex'])
                cleaned_data['height'] = float(cleaned_data.get('height'))  # Default là 0 nếu không có height
                cleaned_data['weight'] = float(cleaned_data.get('weight'))  # Default là 0 nếu không có weight
            except ValueError:
                return None, "Height or weight must be a number", status.HTTP_400_BAD_REQUEST
            
            # Đảm bảo các key bắt buộc tồn tại
            # required_fields = ['name', 'sex', 'born', 'country_noc', 'description', 'special_notes']
            # for field in required_fields:
            #     if field not in cleaned_data or not cleaned_data[field]:
            #         return None, f"{field} is required", status.HTTP_400_BAD_REQUEST

            print(f"Cleaned data: {cleaned_data}")
            
            # Chuẩn bị dữ liệu cho serializer
            created_data = {
                'athlete_id': None,
                'name': cleaned_data['name'],
                'sex': cleaned_data['sex'],
                'born': cleaned_data['born'] if cleaned_data['born'] != '' else 'No information !',
                'height': cleaned_data['height'],
                'weight': cleaned_data['weight'],
                'country_noc': cleaned_data['country_noc'],  # Phải là một giá trị hợp lệ từ bảng Country
                'description': cleaned_data['description'] if cleaned_data['description'] != '' else 'No information !',
                'special_notes': cleaned_data['special_notes'] if cleaned_data['special_notes'] != '' else 'No information !',
            }
            
            print(created_data)

            # Serialize dữ liệu
            serializer = AthleteBioSerializer(data=created_data)
            if serializer.is_valid():
                serializer.save()
                return serializer.data, "Created successfully", status.HTTP_201_CREATED
            else:
                print("Error in serializer validation")
                print(serializer.errors)
                return None, serializer.errors, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
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
        athletes = Athlete_Bio.objects.all()[:20]

        serializer = AthleteBioSerializer(athletes, many=True)
        return serializer.data

    @ staticmethod
    def update(athelet_id, data):
        try:
            athlete = Athlete_Bio.objects.get(athlete_id=athelet_id)
            cleaned_data = data.copy()
            try:
                if cleaned_data['name'] =='':
                    return None, "Name must not be null", status.HTTP_400_BAD_REQUEST
                if cleaned_data['sex'] != 'Male' and cleaned_data['sex'] != 'Female':
                    return None, "Sex must be either Male or Female", status.HTTP_400_BAD_REQUEST
                if cleaned_data['born'] == '':
                    cleaned_data['born'] = 'No information !'
                if cleaned_data['country_noc'] == '':
                    return None, "Country_noc must not be null", status.HTTP_400_BAD_REQUEST
                if cleaned_data['description'] == '':
                    cleaned_data['description'] = 'No information!'
                if cleaned_data['special_notes'] == '':
                    cleaned_data['special_notes'] = 'No information!'
                if cleaned_data['height'] == '0':
                    cleaned_data['height'] = height_process(cleaned_data['country_noc'], cleaned_data['sex'])
                if cleaned_data['weight'] == '0':
                    cleaned_data['weight'] = weight_process(cleaned_data['country_noc'], cleaned_data['sex'])
                cleaned_data['height'] = float(cleaned_data.get('height'))  # Default là 0 nếu không có height
                cleaned_data['weight'] = float(cleaned_data.get('weight'))  # Default là 0 nếu không có weight
            except ValueError:
                return None, "Height or weight must be a number", status.HTTP_400_BAD_REQUEST
            serializer = AthleteBioSerializer(athlete, data=cleaned_data)
            print(cleaned_data)

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

    @ staticmethod
    def delete(id):
        try:
            athlete = Athlete_Bio.objects.get(athlete_id=id)

            if not athlete:
                return None, f"Athlete {id} does not exist", status.HTTP_404_NOT_FOUND

            athlete.delete()
            return None, f"Delete athlete {id} successfully", status.HTTP_200_OK

        except Exception as e:
            return f"An error occurs {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR
