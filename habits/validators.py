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
        if value['execution_time'] > 120:
            raise ValidationError('Время на выполнение привычки не должно превышать 120 секунд')


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
        if value['interval'] > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем раз в 7 дней')
        if value['interval'] < 1:
            raise ValidationError(f'Невозможно выполнять привычку раз в {value["interval"]} дней')
