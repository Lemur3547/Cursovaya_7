import datetime
import json

from django_celery_beat.models import IntervalSchedule, PeriodicTask


def get_interval_and_start_time(habit, interval):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.interval,
        period=IntervalSchedule.DAYS
    )
    today = datetime.datetime.today()
    if datetime.datetime.now().time() > habit.time:
        start_time = datetime.datetime(year=today.year,
                                       month=today.month,
                                       day=today.day + interval,
                                       hour=habit.time.hour,
                                       minute=habit.time.minute)
    else:
        start_time = datetime.datetime(year=today.year,
                                       month=today.month,
                                       day=today.day,
                                       hour=habit.time.hour,
                                       minute=habit.time.minute)
    return schedule, start_time


def create_periodic_task(habit):
    schedule, start_time = get_interval_and_start_time(habit, 1)
    PeriodicTask.objects.create(
        name=f'periodic_task_for_habit_{habit.pk}',
        task="habits.tasks.send_telegram_notification",
        interval=schedule,
        start_time=start_time,
        args=json.dumps([habit.pk])
    )


def update_periodic_task(habit):
    schedule, start_time = get_interval_and_start_time(habit, habit.interval)
    task = PeriodicTask.objects.get(name=f'periodic_task_for_habit_{habit.pk}')
    task.interval = schedule
    task.start_time = start_time
    task.save()


def delete_periodic_task(habit):
    task = PeriodicTask.objects.get(name=f'periodic_task_for_habit_{habit.pk}')
    task.delete()
