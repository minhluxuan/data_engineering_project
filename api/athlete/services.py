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
    database='do_an',
    port=3306,
    charset="utf8mb4",
    collation="utf8mb4_general_ci"
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
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='nhannt',
            database='do_an',
            port=3306,
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )

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

    def searchByName(self, country_id, name):
        try:
            # Try to retrieve the athlete with the given id
            cursor = self.connection.cursor()

            # Fetch paginated data
            query = """
                SELECT * 
                FROM athlete_athlete_bio
                WHERE country_noc_id = %s AND name = %s
            """
            cursor.execute(query, (country_id, name))
            data = cursor.fetchall()
            print(data)

            if data:
                result_list = list()
                columns = ['athlete_id', 'name', 'sex', 'born', 'height', 'weight', 'description', 'special_notes', 'country_noc']
                result_dict = dict(zip(columns, data[0]))
                result_list.append(result_dict)

                # If data is valid, return the serialized data
                return result_list, "Get athlete successfully", status.HTTP_200_OK
            
            else:
                return None, f"Athlete {name} have country_id {country_id} matching query does not exist.", status.HTTP_404_NOT_FOUND

        except Exception as e:
            print(str(e))

            # Catch any other exceptions
            return None, f"An error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR

    def searchByCountryNoc(self, countryNoc, condition_query = 0, page=1, page_size=40, ):
        try:
            # Calculate offset
            offset = (page - 1) * page_size
            
            cursor = self.connection.cursor()
            
            # Fetch total record count
            cursor.execute("SELECT COUNT(*) FROM athlete_athlete_bio WHERE country_noc_id = %s", (countryNoc,))
            total_records = cursor.fetchone()[0]
            
            # Fetch paginated data
            query = """
                    SELECT 
                    ath.*,
                    SUM(CASE WHEN md.medal = 'gold' THEN 1 ELSE 0 END) AS gold,
                    SUM(CASE WHEN md.medal = 'silver' THEN 1 ELSE 0 END) AS silver,
                    SUM(CASE WHEN md.medal = 'bronze' THEN 1 ELSE 0 END) AS bronze
                    FROM 
                        athlete_athlete_bio ath
                    LEFT JOIN 
                        competition_medalresult md 
                        ON md.athlete_id_id = ath.athlete_id
                    WHERE 
                        ath.country_noc_id = %s
                    GROUP BY 
                        ath.athlete_id
                   
                    """
            
            if condition_query == 0:
                query += """LIMIT %s OFFSET %s; """

            elif condition_query == 1:
               query += """
                        HAVING gold > 0 
                        LIMIT %s OFFSET %s;
                        """
            
            elif condition_query == 2:
                query += """
                        HAVING silver > 0 
                        LIMIT %s OFFSET %s;
                        """
            
            elif condition_query == 3:
                query += """
                        HAVING bronze > 0
                        LIMIT %s OFFSET %s;
                        """
            
            print(query)
            cursor.execute(query, (countryNoc, page_size, offset))
            result = cursor.fetchall()

            # Convert result into list of dictionaries
            result_list = []
            columns = ['athlete_id', 'name', 'sex', 'born', 'height', 'weight', 'description', 'special_notes', 'country_noc', 'gold', 'silver', 'bronze']
            for row in result:
                result_dict = dict(zip(columns, row))
                result_list.append(result_dict)
            
            # Calculate total pages
            total_pages = (total_records + page_size - 1) // page_size
            
            return {
                "data": result_list,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_records": total_records,
            }, "Fetched Successfully", status.HTTP_200_OK

        except Exception as e:
            print(str(e))
            return {}, f"Error: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @ staticmethod
    def update(athelet_id, data):
        try:
            print(data)
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
            print(str(e))
            return None, f"An error occurs {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR

    @ staticmethod
    def delete(id):
        try:
            athlete = Athlete_Bio.objects.get(athlete_id=id)
            if not athlete:
                return None, f"Athlete {id} does not exist", status.HTTP_404_NOT_FOUND

            deleted_count, deleted_details  = athlete.delete()

            print(f"Deleted {deleted_count} objects.")
            print(f"Details: {deleted_details}")

            return None, f"Delete athlete {id} successfully", status.HTTP_200_OK

        except Exception as e:
            print(str(e))
            return f"An error occurs {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR
