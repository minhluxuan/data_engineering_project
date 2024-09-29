import requests
import pandas as pd

class CountryOperation:
    base_url = 'http://localhost:8000/countries/'

    def __init__(self):
        pass

    @staticmethod
    def search():
        response = requests.get(CountryOperation.base_url)
        if response:
            return response
        return None
    
class GameOperation:
    base_url = 'http://localhost:8000/games/'
    
    def __init__(self):
        pass

    @staticmethod
    def create(data):
        response = requests.post(GameOperation.base_url, data)
        if response:
            return response
        return None

    @staticmethod
    def search():
        response = requests.get(GameOperation.base_url)
        if response:
            return response
        return None
    
    @staticmethod
    def update(id, data):
        response = requests.put(GameOperation.base_url + str(id) + '/', data)
        if response:
            return response
        return None

    @staticmethod
    def delete(id):
        response = requests.delete(GameOperation.base_url + str(id) + '/')
        if response:
            return response
        return None
