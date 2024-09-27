import requests
import pandas as pd


class MedalTableOperation:
    base_url = 'http://localhost:8000/medaltally/'

    def __init__(self):
        pass

    @staticmethod
    def search(noc=None, edition_id=None):
        params = {}
        if noc:
            params['noc'] = noc
        if edition_id:
            params['edition_id'] = edition_id

        response = requests.get(MedalTableOperation.base_url, params=params)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df['total'] = df[['gold', 'silver', 'bronze']].sum(axis=1)
            return df
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    @staticmethod
    def create(data):
        response = requests.post(MedalTableOperation.base_url, json=data)
        if response.status_code == 201:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    @staticmethod
    def update(id, data):
        response = requests.put(
            f"{MedalTableOperation.base_url}{id}/", json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    @staticmethod
    def delete(id):
        response = requests.delete(f"{MedalTableOperation.base_url}{id}/")
        if response.status_code == 204:
            return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
