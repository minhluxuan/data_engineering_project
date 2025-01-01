import requests


class AthleteOperations():
    base_url = 'http://localhost:8000/athlete_bio/'
    base_url_update = 'http://localhost:8000/athlete_bio_update/'

    def __init__(self):
        pass

    @staticmethod
    def create(data):
        response = requests.post(AthleteOperations.base_url, data)
        if response:
            return response
        return None

    @staticmethod
    def search(option, country_id, page_size):
        response = requests.get(AthleteOperations.base_url + str(option) + '/', params= {'country_id': country_id, 'page': page_size})
        if response:
            return response
        return None

    @staticmethod
    def searchOne(option, name, country_id):
        response = requests.get(AthleteOperations.base_url + str(option) + '/', params= {'country_id': country_id, 'name': name})
        return response
    
    @staticmethod
    def delete(id):
        response = requests.delete(AthleteOperations.base_url_update + str(id) + '/')
        print(response)
        if response.status_code != 500:
            return response
        return None

    @staticmethod
    def update(id, data):
        response = requests.put(
            AthleteOperations.base_url_update + str(id) + '/', json=data)
        if response.status_code != 500:
            print(response)
            return response
        return None


if __name__ == '__main__':
    print(AthleteOperations().search())
