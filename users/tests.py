import pytz
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


# Create your tests here.
class UserTestCase(APITestCase):
    def test_register_habit(self):
        response = self.client.post(
            '/users/register/',
            data={
                "email": "test@email.com",
                "password": "password"
            }
        )
        newuser = User.objects.get(email='test@email.com')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            newuser.__str__(),
            'test@email.com'
        )
        date_joined = newuser.date_joined.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime(
            "%Y-%m-%dT%H:%M:%S.%f%z")
        date_joined = f"{date_joined[:-2]}:{date_joined[-2:]}"
        self.assertEqual(
            response.json(),
            {
                "id": newuser.pk,
                "password": newuser.password,
                "last_login": None,
                "is_superuser": False,
                "first_name": "",
                "last_name": "",
                "is_staff": False,
                "is_active": False,
                "date_joined": date_joined,
                "email": "test@email.com",
                "tg_chat_id": None,
                "groups": [],
                "user_permissions": []
            }
        )

    def test_register_habit_exception(self):
        response = self.client.post(
            '/users/register/',
            data={
                "email": "test@email.com",
                "password": "password",
                "is_staff": True,
                "is_superuser": True
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя использовать поля is_staff и is_superuser.']}
        )

        response = self.client.post(
            '/users/register/',
            data={
                "email": "test@email.com",
                "password": "password",
                "is_staff": True
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя использовать поле is_staff.']}
        )

        response = self.client.post(
            '/users/register/',
            data={
                "email": "test@email.com",
                "password": "password",
                "is_superuser": True
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя использовать поле is_superuser.']}
        )
