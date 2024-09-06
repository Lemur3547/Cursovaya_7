from rest_framework import serializers

from habits.models import Habit
from habits.validators import RewardValidator, ExecutionTimeValidator, IsAssociatedHabitPleasant, IntervalValidator, \
    TimeValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [RewardValidator(), ExecutionTimeValidator(), IsAssociatedHabitPleasant(), IntervalValidator(),
                      TimeValidator()]
