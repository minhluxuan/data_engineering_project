import requests


class AthleteOperations():
  base_url = 'http://localhost:8000/athlete_bio/'

  def __init__(self):
    pass

  @staticmethod
  def create(data):
    response = requests.post(AthleteOperations.base_url, data)
    if response:
      return response
    return None

  @staticmethod
  def search():
    response = requests.get(AthleteOperations.base_url)
    if response:
      return response
    return None
  
  @staticmethod
  def searchOne(id):
    response = requests.get(AthleteOperations.base_url + str(id) + '/')
    if response.status_code != 500:
      return response
    return None

  @staticmethod
  def delete(id):
    response = requests.delete(AthleteOperations.base_url + str(id) + '/')
    print(response)
    if response.status_code != 500:
      return response
    return None

  @staticmethod
  def update(id, data):
    response = requests.put(AthleteOperations.base_url + str(id) + '/', json = data)
    if response != 500:
      return response
    return None

  