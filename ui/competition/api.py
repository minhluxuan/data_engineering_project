import requests
import pandas as pd

class EventResultOperation:
    base_url = 'http://localhost:8000/eventResult/'

    def __init__(self):
        pass

    @staticmethod
    def create(data):
        response = requests.post(EventResultOperation.base_url, data)
        if response:
            return response
        return None

    @staticmethod
    def search():
        response = requests.get(EventResultOperation.base_url)
        if response:
            return response
        return None
    
    @staticmethod
    def update(id1, id2, id3, id4, data):
        # Tạo URL cho yêu cầu PUT với các ID
        url = f"{EventResultOperation.base_url}{id1}-{id2}-{id3}-{id4}/"
        response = requests.put(url, json=data)
        if response.ok:
            return response.json()
        return None

    @staticmethod
    def delete(id1, id2, id3, id4):
        # Tạo URL cho yêu cầu DELETE với các ID
        url = f"{EventResultOperation.base_url}{id1}-{id2}-{id3}-{id4}/"
        response = requests.delete(url)
        if response.ok:  # Kiểm tra xem phản hồi có thành công không
            return response.json()  # Trả về dữ liệu JSON nếu có
        return None  # Nếu không thành công, trả về None
