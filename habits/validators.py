from rest_framework.exceptions import ValidationError

from habits.models import Habit


def validate_related_habit_and_reward(data):
    if data.get("related_habit") and data.get("reward"):
        raise ValidationError(
            "Нельзя одновременно выбрать связанную привычку и указать вознаграждение"
        )


def validate_duration(duration):
    """
    Валидация продолжительности
    """
    if not 1 < duration <= 120:
        raise ValidationError("Время выполнения не должно превышать 120 сек")


def validate_related_habit(data):
    """Ф-ция, которая проверяет корректность связанной привычки."""
    related_habit = data.get("related_habit")
    if related_habit:
        habit = Habit.objects.get(pk=related_habit.pk)

        # Если это поле False (т.е. привычка полезная, а не приятная),
        # Валидатор выбрасывает исключение ValidationError(чтобы нельзя было свзять две полезные привычки)
        if not habit.pleasant_habit:
            raise ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки"
            )


def validate_pleasant_habit(data):
    if data.get("pleasant_habit") and (data.get("related_habit") or data.get("reward")):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки"
        )


def validate_periodicity(periodicity):
    """
    Валидация периодичности
    """
    if periodicity > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в неделю")
