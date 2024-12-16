from datetime import datetime, timedelta
import pytz
from celery import shared_task
from config import settings
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_reminder():
    """За 30 минут до начала привычки отправляем сообщение в тг"""

    habits = Habit.objects.all()

    tz = pytz.timezone(settings.TIME_ZONE)  # получение часовой зоны из settings
    print(f"Тайм зона: {tz}")

    now_local = datetime.now(tz)  # текущее время из now()
    print(f"Текущее время: {now_local}")

    for habit in habits:

        # время оповещения(мы вычитаем от времени начала привычки 30 минут)
        notification_time = habit.time - timedelta(minutes=30)

        if now_local >= notification_time:
            user_tg = habit.user.telegram_id  # Телеграм ID пользователя

            message = (
                f"Не забудь!\n"
                f"Действие: {habit.action}\n"
                f"Место: {habit.place}\n"
                f"Через 30 минут."
            )

            send_telegram_message(user_tg, message)

            if habit.reward:
                send_telegram_message(
                    user_tg,
                    f"Молодец! Ты заслужил награду: {habit.reward} после {habit.action}",
                )

            # Обновление времени выполнения привычки на сутки (чтобы только одно сообщение в день приходило)
            habit.time += timedelta(days=habit.periodicity)
            habit.save()
