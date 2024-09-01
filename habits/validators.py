from rest_framework.exceptions import ValidationError


class RewardValidator:
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('associated_habit') or value.get('reward'):
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')
        else:
            if value.get('associated_habit') and value.get('reward'):
                raise ValidationError('Нельзя выбрать связанную привычку и вознаграждение одновременно')
            if value.get('associated_habit') is None and value.get('reward') is None:
                raise ValidationError('Выберите связанную привычку или вознаграждение')


class ExecutionTimeValidator:
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('execution_time'):
                raise ValidationError("Для приятной привычки не требуется длительность (execution_time)")
        else:
            if value.get('execution_time'):
                if value.get('execution_time') > 120:
                    raise ValidationError('Время на выполнение привычки не должно превышать 120 секунд')
                if value.get('execution_time') < 1:
                    raise ValidationError(
                        f'Время на выполнение привычки не не может быть {value["execution_time"]} секунд')
            else:
                raise ValidationError('Заполните поле execution_time')


class IsAssociatedHabitPleasant:
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('associated_habit') and not value.get('is_pleasant'):
            if not value.get('associated_habit').is_pleasant:
                raise ValidationError('В связанные привычки могут попадать только приятные привычки')


class IntervalValidator:
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('interval'):
                raise ValidationError("Для приятной привычки не требуется интервал (interval)")
        else:
            if value.get('interval'):
                if value.get('interval') > 7:
                    raise ValidationError('Нельзя выполнять привычку реже, чем раз в 7 дней')
                if value.get('interval') < 1:
                    raise ValidationError(f'Невозможно выполнять привычку раз в {value["interval"]} дней')
            else:
                raise ValidationError('Заполните поле interval')


class TimeValidator:
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_pleasant'):
            if value.get('time'):
                raise ValidationError("Для приятной привычки не требуется время (time)")
        else:
            if not value.get('time'):
                raise ValidationError("Заполните поле time")
