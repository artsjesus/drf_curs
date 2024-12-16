from django.urls import path
from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
    MyHabitsListView,
    PublicListAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("create/", HabitCreateAPIView.as_view(), name="create"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="habit_delete"),
    path("my_habits/", MyHabitsListView.as_view(), name="my_habits"),
    path("public/", PublicListAPIView.as_view(), name="public"),
]
