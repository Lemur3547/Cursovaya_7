import requests

from celery import shared_task
from django.conf import settings

from habits.models import Habit


@shared_task
def send_telegram_notification(habit_pk):
    habit = Habit.objects.get(pk=habit_pk)
    if habit.associated_habit:
        reward = habit.associated_habit.action
    else:
        reward = habit.reward
    message = (f"Выполните полезную привычку!\n"
               f"Вы должны {habit.action} в {habit.time.strftime('%H:%M')} в {habit.place}\n"
               f"Время выполнения привычки составит {habit.execution_time} секунд\n"
               f"В награду вы можете {reward}")
    if habit.user.tg_chat_id:
        chat_id = habit.user.tg_chat_id
        params = {
            'text': message,
            'chat_id': chat_id
        }
        requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
