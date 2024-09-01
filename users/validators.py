from rest_framework.exceptions import ValidationError


class RegistrationValidator:
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if len(value) > 2:
            raise ValidationError('Введите только email и пароль.')
