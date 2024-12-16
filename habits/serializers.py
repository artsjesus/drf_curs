from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
    validate_duration,
    validate_periodicity,
    validate_related_habit_and_reward,
    validate_related_habit,
    validate_pleasant_habit,
)


class HabitSerializer(ModelSerializer):
    """
    Сериалайзер привычки
    """

    duration = serializers.IntegerField(validators=[validate_duration])
    periodicity = serializers.IntegerField(validators=[validate_periodicity])

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        validate_related_habit_and_reward(data)
        validate_related_habit(data)
        validate_pleasant_habit(data)

        return data
