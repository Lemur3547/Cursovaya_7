from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitsPaginator
from habits.serializers import HabitSerializer
from habits.services import create_periodic_task, update_periodic_task, delete_periodic_task
from users.permissions import IsOwner


# Create your views here.
class HabitCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()
        if not habit.is_pleasant:
            create_periodic_task(habit)


class HabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator

    def get_queryset(self):
        queryset = Habit.objects.filter(user=self.request.user)
        return queryset


class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPaginator


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PublicHabitRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [IsAuthenticated]


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        habit = serializer.save()
        if not habit.is_pleasant:
            update_periodic_task(habit)


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        if not instance.is_pleasant:
            delete_periodic_task(instance)
        instance.delete()
