from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Role
from ..serializers import UserSerializer


class UserCreateTests(APITestCase):
    def setUp(self):
        Role.objects.create(name="Admin")

        user_1 = {
            'email': "ahmed.o@e360africa.com",
            'first_name': 'Ahmed',
            'last_name': 'Ojo',
            'role_id': 1
        }
        get_user_model().objects.create_user(**user_1)
        #self.authenticator()

    # def authenticator(self):
    #     url = reverse('login')
    #     data = {
    #         'email': 'ahmed.o@e360africa.com',
    #         'password': 'password'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     token = response.json()['access']
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_can_create_user(self):
        url = reverse('user_sign_up')
        data = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'role_id': 1,
            'phone_number': "08146646207",
            'password': "newpassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(get_user_model().objects.last().email, 'rahman.s@e360africa.com')
        self.assertTrue(get_user_model().objects.last().check_password('newpassword'))


class UserRetrieveUpdateDeleteTests(APITestCase):

    def setUp(self):
        Role.objects.create(name="Admin")
        data_1 = {
                'email': "rahman.s@e360africa.com",
                'first_name': 'Rahman',
                'last_name': 'Solanke',
                'phone_number': "08146646207",
                'role_id': 1
            }
        data_2 = {
                'email': "ahmed.o@e360africa.com",
                'first_name': 'Ahmed',
                'last_name': 'Ojo',
                'phone_number': "08146646209",
                'role_id': 1
            }
        data_3 = {
                'email': "Nonso.m@e360africa.com",
                'first_name': 'Nonso',
                'last_name': 'Mgbechi',
                'phone_number': "08146646212",
                'role_id': 1
            }

        user_1 = get_user_model().objects.create_user(**data_1)
        user_2 = get_user_model().objects.create_user(**data_2)
        user_3 = get_user_model().objects.create_user(**data_3)
        
        # self.authenticator()


    # def authenticator(self):
    #     url = reverse('login')
    #     data = {
    #         'email': 'rahman.s@e360africa.com',
    #         'password': 'password'
    #     }
    #     response = self.client.post(url, data, format='json')
    #     token = response.json()['access']
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_all_users(self):
        url = reverse('all_users')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_user(self):
        url = reverse('user_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)
    
    def test_get_invalid_user(self):
        url = reverse('user_detail', kwargs={'pk': 20})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_user_default_password(self):
        emp = get_user_model().objects.get(pk=1)
        emp2 = get_user_model().objects.get(pk=2)
        emp3 = get_user_model().objects.get(pk=3)
        self.assertTrue(emp.check_password('password'))
        self.assertTrue(emp2.check_password('password'))
        self.assertTrue(emp3.check_password('password'))

    def test_can_not_get_inactive_user_detail(self):
        user = get_user_model().objects.get(pk=1)
        user.is_active = False
        user.save()
        url = reverse('user_detail', kwargs={'pk': 1})
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_update_user(self):
        url = reverse('user_detail', kwargs={'pk': 1})
        response = self.client.patch(url, {'phone_number': '09809883883'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['phone_number'], '09809883883')
    
    def test_can_do_multiple_updates_user(self):
        url = reverse('user_detail', kwargs={'pk': 3})
        response = self.client.patch(url, {'phone_number': '09809883883', 'email':'Nonso.omo@e360africa.com'},
                                    format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['phone_number'], '09809883883')
        self.assertEqual(data['email'], 'Nonso.omo@e360africa.com')

    def test_invalid_update_user(self):
        url = reverse('user_detail', kwargs={'pk': 2})
        response = self.client.patch(url, {'description': 'Now a junior dev', 'email':'ahmed.o'},
                                    format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        