from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Role
#from ..serializers import EmployeeSerializer


class UserCreateModelTest(APITestCase):
    """
    Test module for user model exists
    """
    def test_can_create_user_in_db(self):
        user = get_user_model().objects.create_user(email="rahman.s@e360africa.com", first_name="Rahman",
        phone_number="08146646207", last_name="Solanke")
        self.assertIsNotNone(user)


class RoleCreateModelTest(APITestCase):
    def test_can_create_role(self):
        self.assertIsNotNone(Role.objects.create(name="Admin"))
        self.assertEqual(Role.objects.count(), 1)
        role = Role.objects.get(pk=1)
        self.assertEqual(role.name, "Admin")


class UserModelTest(APITestCase):
    """
    Test module for Employee Model functionality
    """
    def setUp(self):
        user_1 = {
            'email': "rahman.s@e360africa.com",
            'phone_number': "08146646207",
            'first_name': 'Rahman',
            'last_name': 'Solanke'
        }
        user_2 = {
            'email': "ahmed.o@e360africa.com",
            'phone_number': "08146646208",
            'first_name': 'Ahmed',
            'last_name': 'Ojo',
        }
        user_1 = get_user_model().objects.create_user(**user_1)
        user_2 = get_user_model().objects.create_user(**user_2)

    def test_users_created(self):
        self.assertEqual(get_user_model().objects.count(), 2)
    
    def test_users_details(self):
        user_1 = get_user_model().objects.get(pk=1)
        user_2 = get_user_model().objects.get(pk=2)
        self.assertEqual(user_1.email, 'rahman.s@e360africa.com')
        self.assertEqual(user_2.email, 'ahmed.o@e360africa.com')

        self.assertTrue(user_1.is_active)
        self.assertTrue(user_2.is_active)

        self.assertEqual(user_1.first_name, 'Rahman')
        self.assertEqual(user_2.last_name, 'Ojo')

        self.assertIsNone(user_1.last_login)
        self.assertTrue(user_1.check_password('password'))

        self.assertIsNone(user_1.role)

