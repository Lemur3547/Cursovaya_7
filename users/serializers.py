from rest_framework import serializers

from users.models import User
from users.validators import RegistrationValidator


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        validators = [RegistrationValidator()]
