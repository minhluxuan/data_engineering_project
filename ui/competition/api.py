import requests
import pandas as pd


class EventResultOperation:

    base_url = 'http://localhost:8000/eventresult/'

    def __init__(self):
        pass

    @staticmethod
    def create(data):
        response = requests.post(EventResultOperation.base_url, data)
        if response:
            return response
        return None

    @staticmethod
    def search(edition_id, country_noc, result_id, athlete_id):
        url = f"{EventResultOperation.base_url}{
            edition_id}-{country_noc}-{result_id}-{athlete_id}/"
        response = requests.get(url)
        if response:
            return response
        return None

    @staticmethod
    def update(edition_id, country_noc, result_id, athlete_id, data):
        # Tạo URL cho yêu cầu PUT với các ID
        url = f"{
            EventResultOperation.base_url}u/{edition_id}-{country_noc}-{result_id}-{athlete_id}/"
        response = requests.put(url, json=data)
        if response.ok:
            return response
        return None

    @staticmethod
    def delete(id1, id2, id3, id4):
        # Tạo URL cho yêu cầu DELETE với các ID
        url = f"{EventResultOperation.base_url}d/{id1}-{id2}-{id3}-{id4}/"
        response = requests.delete(url)
        if response.ok:  # Kiểm tra xem phản hồi có thành công không
            return response  # Trả về dữ liệu JSON nếu có
        return None  # Nếu không thành công, trả về None


class ResultOperation:
    base_url = 'http://localhost:8000/results/'

    def __init__(self):
        pass

    @staticmethod
    def create(data):
        response = requests.post(ResultOperation.base_url, data)
        if response:
            return response
        return None

    @staticmethod
    def search():
        response = requests.get(ResultOperation.base_url)
        if response:
            return response
        return None

    @staticmethod
    def update(id, data):
        response = requests.put(ResultOperation.base_url + str(id) + '/', data)
        print(response)
        if response:
            return response
        return None

    @staticmethod
    def delete(id):
        response = requests.delete(ResultOperation.base_url + str(id))
        print(response)
        if response:
            return response
        return None
