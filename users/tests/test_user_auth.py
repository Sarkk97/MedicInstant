from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.test import APITestCase

from ..models import Role

class UserAuthentication(APITestCase):
    def setUp(self):
        Role.objects.create(name="Admin")
        data = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'role_id': 1,
            'phone_number': "08146646207"
        }
        get_user_model().objects.create_user(**data)

    def test_user_login(self):
        url = reverse('login')
        data = {
            'email': 'rahman.s@e360africa.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_last_login_time_change_after_login(self):
        url = reverse('login')
        data = {
            'email': 'rahman.s@e360africa.com',
            'password': 'password'
        }
        self.client.post(url, data, format='json')
        user = get_user_model().objects.get(email="rahman.s@e360africa.com")
        self.assertIsNotNone(user.last_login)
