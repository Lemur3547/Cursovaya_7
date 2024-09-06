import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.tasks import send_telegram_notification
from users.models import User


# Create your tests here.
class HabitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@test.com', tg_chat_id=1403453241)
        self.associated_habit = Habit.objects.create(
            user=self.user,
            place='test place',
            action='test action',
            is_pleasant=True,
            is_public=False
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='test place',
            time=datetime.datetime(2024, 9, 5, 20, 5, 46),
            action='test action',
            is_pleasant=False,
            associated_habit=self.associated_habit,
            interval=2,
            execution_time=100,
            is_public=False
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 100,
                "interval": 2,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.habit.pk + 1,
                "place": "test place",
                "time": "12:34:00",
                "action": "test action",
                "is_pleasant": False,
                "interval": 2,
                "reward": None,
                "execution_time": 100,
                "is_public": False,
                "user": self.user.pk,
                "associated_habit": self.associated_habit.pk
            }
        )

    def test_list_habit(self):
        """Тестирование просмотра списка привычек"""
        response = self.client.get(
            '/habits/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.associated_habit.pk,
                        "place": "test place",
                        "time": None,
                        "action": "test action",
                        "is_pleasant": True,
                        "interval": None,
                        "reward": None,
                        "execution_time": None,
                        "is_public": False,
                        "user": self.user.pk,
                        "associated_habit": None
                    },
                    {
                        "id": self.habit.pk,
                        "place": "test place",
                        "time": "20:05:46",
                        "action": "test action",
                        "is_pleasant": False,
                        "interval": 2,
                        "reward": None,
                        "execution_time": 100,
                        "is_public": False,
                        "user": self.user.pk,
                        "associated_habit": self.associated_habit.pk
                    }
                ]
            }
        )

    def test_retrieve_habit(self):
        """Тестирование просмотра одной привычки"""
        response = self.client.get(
            reverse('habits:habit_view', args=(self.habit.pk,)),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.habit.pk,
                "place": "test place",
                "time": "20:05:46",
                "action": "test action",
                "is_pleasant": False,
                "interval": 2,
                "reward": None,
                "execution_time": 100,
                "is_public": False,
                "user": self.user.pk,
                "associated_habit": self.associated_habit.pk
            }
        )
        self.assertEqual(
            self.habit.__str__(),
            "test action"
        )

    def test_update_habit_before_now(self):
        """Тестирование изменения привычки"""
        self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 100,
                "interval": 2,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk
            }
        )
        response = self.client.patch(
            reverse('habits:habit_update', args=(self.habit.pk+1,)),
            data={
                "place": "upd place",
                "time": "00:00",
                "action": "upd action",
                "interval": 2,
                "execution_time": 100,
                "associated_habit": self.associated_habit.pk
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.habit.pk+1,
                "place": "upd place",
                "time": "00:00:00",
                "action": "upd action",
                "is_pleasant": False,
                "interval": 2,
                "reward": None,
                "execution_time": 100,
                "is_public": False,
                "user": self.user.pk,
                "associated_habit": self.associated_habit.pk
            }
        )

    def test_update_habit_after_now(self):
        """Тестирование изменения привычки"""
        self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 100,
                "interval": 2,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk
            }
        )
        response = self.client.patch(
            reverse('habits:habit_update', args=(self.habit.pk+1,)),
            data={
                "place": "upd place",
                "time": "23:59:59",
                "action": "upd action",
                "interval": 2,
                "execution_time": 100,
                "associated_habit": self.associated_habit.pk
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": self.habit.pk+1,
                "place": "upd place",
                "time": "23:59:59",
                "action": "upd action",
                "is_pleasant": False,
                "interval": 2,
                "reward": None,
                "execution_time": 100,
                "is_public": False,
                "user": self.user.pk,
                "associated_habit": self.associated_habit.pk
            }
        )

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 100,
                "interval": 2,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk
            }
        )
        response = self.client.delete(
            reverse('habits:habit_delete', args=(self.habit.pk+1,)),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_delete_pleasant_habit(self):
        """Тестирование удаления полезной привычки"""
        response = self.client.delete(
            reverse('habits:habit_delete', args=(self.associated_habit.pk,)),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_reward_validator(self):
        """Тестирование валидатора вознаграждения"""
        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": True,
                "is_public": False,
                "associated_habit": self.associated_habit.pk
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "associated_habit": self.associated_habit.pk,
                "reward": "test reward",
                "execution_time": 100,
                "interval": 2,
                "time": "12:34"
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя выбрать связанную привычку и вознаграждение одновременно']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 100,
                "interval": 2,
                "time": "12:34"
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Выберите связанную привычку или вознаграждение']}
        )

    def test_execution_time_validator(self):
        """Тестирование валидатора времени выполнения"""
        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": True,
                "is_public": False,
                "execution_time": 100
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Для приятной привычки не требуется длительность (execution_time)']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "associated_habit": self.associated_habit.pk,
                "execution_time": -10,
                "interval": 2,
                "time": "12:34"
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Время на выполнение привычки не не может быть -10 секунд']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 150,
                "interval": 2,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk,
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Время на выполнение привычки не должно превышать 120 секунд']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "interval": 2,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk,
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Заполните поле execution_time']}
        )

    def test_associated_habit_validator(self):
        """Тестирование валидатора связанной привычки"""
        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "associated_habit": self.habit.pk,
                "execution_time": 100,
                "interval": 2,
                "time": "12:34"
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {
                "non_field_errors": [
                    "В связанные привычки могут попадать только приятные привычки"
                ]
            }
        )

    def test_interval_validator(self):
        """Тестирование валидатора интервала"""
        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": True,
                "is_public": False,
                "interval": 2
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Для приятной привычки не требуется интервал (interval)']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "associated_habit": self.associated_habit.pk,
                "execution_time": 100,
                "interval": 10,
                "time": "12:34"
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя выполнять привычку реже, чем раз в 7 дней']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 100,
                "interval": -2,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk,
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Невозможно выполнять привычку раз в -2 дней']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "execution_time": 100,
                "time": "12:34",
                "associated_habit": self.associated_habit.pk,
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Заполните поле interval']}
        )

    def test_time_validator(self):
        """Тестирование валидатора времени"""
        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": True,
                "is_public": False,
                "time": "12:34"
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Для приятной привычки не требуется время (time)']}
        )

        response = self.client.post(
            '/habits/create/',
            data={
                "place": "test place",
                "action": "test action",
                "is_pleasant": False,
                "is_public": False,
                "associated_habit": self.associated_habit.pk,
                "execution_time": 100,
                "interval": 2
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Заполните поле time']}
        )

    def test_send_telegram_notification(self):
        """Тестирование отправки уведомлений в телеграм"""
        send_telegram_notification(self.habit.pk)
        self.habit.associated_habit = None
        self.habit.reward = 'test reward'
        self.habit.save()
        send_telegram_notification(self.habit.pk)
