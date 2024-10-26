from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import EventResult, MedalResult

class EventResultViewTest(APITestCase):

    def setUp(self):
        # Tạo dữ liệu mẫu cho test
        self.event_result = EventResult.objects.create(
            edition_id=1,
            country_noc='USA',
            sport='Basketball',
            event='Final',
            result_id=1,
            athlete_id=1,
            pos=1,
            isTeamSport=False
        )
        self.medal_result = MedalResult.objects.create(
            edition_id=1,
            country_noc='USA',
            result_id=1,
            athlete_id=1,
            medal='Gold'
        )

    def test_create_event_result(self):
        url = reverse('event_result_post')
        data = {
            'edition_id': 2,
            'country_noc': 'USA',
            'sport': 'Soccer',
            'event': 'Final',
            'result_id': 2,
            'athlete_id': 2,
            'pos': 2,
            'isTeamSport': False,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_event_results(self):
        url = reverse('event_result_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
