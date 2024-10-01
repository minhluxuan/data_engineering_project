import requests
import pandas as pd

 
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
