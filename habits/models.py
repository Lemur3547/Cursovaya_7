from django.conf import settings
from django.db import models

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             **NULLABLE)
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(verbose_name='Приятная привычка')
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
    interval = models.SmallIntegerField(verbose_name='Периодичность (дней)')
    reward = models.CharField(max_length=255, verbose_name='Вознаграждение', **NULLABLE)
    execution_time = models.SmallIntegerField(verbose_name='Время на выполнение (в секундах)')
    is_public = models.BooleanField(verbose_name='Публичная привычка')
