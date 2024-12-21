from .serializers import ResultSerializer
from .models import Result
import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EventResult, MedalResult
from .serializers import EventResultSerializer, MedalResultSerializer


class EventResultService:
    def __init__(self):
        pass

    @staticmethod
    def search(result_id, athlete_id):
        queryset = EventResult.objects.all()
        if result_id != -793654029:
            queryset = queryset.filter(result_id_id=result_id)
        if athlete_id != -793654029:
            queryset = queryset.filter(athlete_id_id=athlete_id)
        # Trả về None nếu không có kết quả
        if not queryset.exists():
            return None
        # Truy vấn MedalResult liên quan đến các EventResult đã lọc
        event_results_with_medals = []
        for event_result in queryset:
            try:
                medal_result = MedalResult.objects.get(
                    result_id_id=result_id,
                    athlete_id_id=athlete_id
                )
                # Thêm vào danh sách với 'medal' nằm trong cùng đối tượng
                event_results_with_medals.append({
                    'result_id': event_result.result_id_id,
                    'athlete_id': event_result.athlete_id_id,
                    'pos': event_result.pos,
                    'isTeamSport': event_result.isTeamSport,
                    'medal': medal_result.medal  # Chỉ lấy giá trị của medal
                })
            except MedalResult.DoesNotExist:
                # Nếu không tìm thấy huy chương, thêm 'medal': None
                event_results_with_medals.append({
                    'result_id': event_result.result_id_id,
                    'athlete_id': event_result.athlete_id_id,
                    'pos': event_result.pos,
                    'isTeamSport': event_result.isTeamSport,
                    'medal': None
                })
        # Trả về dữ liệu đã kết hợp
        print(event_results_with_medals)
        return event_results_with_medals, "Search successfully", status.HTTP_200_OK

    @staticmethod
    def update(result_id, athlete_id, data):
        try:
            # Tìm event_result theo 4 id
            event_res = EventResult.objects.get(result_id=result_id, athlete_id=athlete_id)
            # Tách dữ liệu thành hai phần
            event_data = {
                # Nếu không có, dùng giá trị hiện tại
                'result_id': data.get('result_id', event_res.result_id_id),
                'athlete_id': data.get('athlete_id', event_res.athlete_id_id),
                'pos': data.get('pos', event_res.pos),
                'isTeamSport': data.get('isTeamSport', event_res.isTeamSport),
            }
            # Cập nhật EventResult
            event_serializer = EventResultSerializer(
                event_res, data=event_data, partial=True)
            if event_serializer.is_valid():
                event_serializer.save()  # Lưu event_result đã cập nhật
            else:
                return None, event_serializer.errors, status.HTTP_400_BAD_REQUEST
            # Cập nhật MedalResult nếu có
            # Chỉ cập nhật nếu medal không phải là None
            if 'medal' in data and data['medal'] is not None:
                try:
                    medal_result = MedalResult.objects.get(
                        result_id=result_id,
                        athlete_id=athlete_id
                    )
                    medal_data = {
                        'result_id': data.get('result_id', medal_result.result_id),
                        'athlete_id': data.get('athlete_id', medal_result.athlete_id),
                        # Chỉ cập nhật medal nếu có giá trị
                        'medal': data['medal'],
                    }
                    medal_serializer = MedalResultSerializer(
                        medal_result, data=medal_data, partial=True)
                    if medal_serializer.is_valid():
                        medal_serializer.save()  # Lưu medal_result đã cập nhật
                    else:
                        return None, medal_serializer.errors, status.HTTP_400_BAD_REQUEST
                except MedalResult.DoesNotExist:
                    return None, "Medal result not found", status.HTTP_404_NOT_FOUND
            return event_serializer.data, "Update successfully", status.HTTP_200_OK
        except EventResult.DoesNotExist:
            return None, "Event result not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return None, f"An error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create(data):
        print(data.get('isTeamSport'))
        try:
            # Tách data
            event_data = {
                'id': None,
                'result_id': data.get('result_id'),
                'athlete_id': data.get('athlete_id'),
                'pos': data.get('pos') if data.get('pos') != '' else None,
                'isTeamSport': 1 if data.get('isTeamSport') else 0,
            }
            medal_data = {
                'id': None,
                'result_id': data.get('result_id'),
                'athlete_id': data.get('athlete_id'),
                'medal': data.get('medal'),
            }
            # Create cho event
            serializer = EventResultSerializer(data=event_data)
            if serializer.is_valid():
                serializer.save()  # Lưu event_result mới
                # Tạo medal
                if medal_data.get('medal') is not None:
                    medal_serializer = MedalResultSerializer(data=medal_data)
                    if medal_serializer.is_valid():
                        medal_serializer.save()  # Lưu medal_result mới
                    else:
                        return None, medal_serializer.errors, status.HTTP_400_BAD_REQUEST
                return serializer.data, "Create successfully", status.HTTP_201_CREATED
            else:
                return None, serializer.errors, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            return None, f"An error occurred: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def delete(edition_id, country_noc, result_id, athlete_id):
        try:
            # Tìm và xóa tất cả MedalResult liên quan
            MedalResult.objects.filter(
                result_id=result_id,
                athlete_id=athlete_id
            ).delete()

            # Tìm và xóa EventResult
            event_result = EventResult.objects.get(
                result_id=result_id,
                athlete_id=athlete_id
            )
            event_result.delete()

            # Trả về đủ 3 giá trị
            return None, "Event result deleted successfully.", status.HTTP_204_NO_CONTENT
        except EventResult.DoesNotExist:
            return None, "Event result not found.", status.HTTP_404_NOT_FOUND  # Trả về đủ 3 giá trị
        except Exception as e:
            # Trả về đủ 3 giá trị
            return None, str(e), status.HTTP_500_INTERNAL_SERVER_ERROR

    def __str__():
        return "Done"


class ResultService:
    def __init__(self):
        pass

    @staticmethod
    def create(data):
        print("I'm hear")
        print(data)
        try:
            cleaned_data = {
                key: value[0] if isinstance(value, list) else value
                for key, value in data.items()
            }
            processed_data = cleaned_data.copy()
            processed_data['result_id'] = None
            processed_data['result_participants'] = 0
            processed_data['sport_url'] = processed_data['sport_url'] if processed_data['sport_url'] else None
            processed_data['result_format'] = processed_data['result_format'] if processed_data['result_format'] else None
            processed_data['result_detail'] = processed_data['result_detail'] if processed_data['result_detail'] else None
            processed_data['result_description'] = processed_data['result_description'] if processed_data['result_description'] else None
            print(processed_data)
            serializer = ResultSerializer(data=processed_data)
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
    def update(result_id, data):
        try:
            print(data)
            result = Result.objects.get(result_id = result_id)
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
