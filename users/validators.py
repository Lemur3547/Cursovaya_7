from rest_framework.exceptions import ValidationError


class RegistrationValidator:
    def __init__(self):
        pass

    def __call__(self, value, *args, **kwargs):
        if value.get('is_staff') and value.get('is_superuser'):
            raise ValidationError('Нельзя использовать поля is_staff и is_superuser.')
        if value.get('is_staff'):
            raise ValidationError('Нельзя использовать поле is_staff.')
        if value.get('is_superuser'):
            raise ValidationError('Нельзя использовать поле is_superuser.')
