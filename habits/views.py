from django.utils.timezone import now
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habit
from habits.pagination import MyPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """
    Создание привычек
    """

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        started_at = serializer.validated_data.get("started_at", now().date())
        serializer.save(user=self.request.user, started_at=started_at)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    Изменение привычки
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление привычки
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class MyHabitsListView(generics.ListAPIView):
    """
    Список собственных привычек
    """

    serializer_class = HabitSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by("time")


class PublicListAPIView(generics.ListAPIView):
    """Список публичных привычек."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = (AllowAny,)
    pagination_class = MyPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by("time")
