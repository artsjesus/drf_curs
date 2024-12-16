from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from users.models import User


class HabitAPITests(APITestCase):
    def setUp(self):
        """Некая фикстура для тестов всех методов"""
        self.user = User.objects.create(email="admin@mail.ru", password="123")
        self.habit = Habit.objects.create(
            user=self.user,
            place="Спортзал",
            time="2024-12-11 17:27:00+03",
            duration=30,
            periodicity=1,
            action="Тренировки",
            pleasant_habit=True,
            reward=None,
            is_public=True,
        )
        self.create_url = "/habits/create/"
        self.update_url = f"/habits/{self.habit.pk}/update/"
        self.delete_url = f"/habits/{self.habit.pk}/delete/"
        self.my_habits_url = "/habits/my_habits/"
        self.public_url = "/habits/public/"
        self.client.force_authenticate(user=self.user)

    def test_habit_create(self):
        """Тест на создание привычки, и проверки кол-ва в базе"""
        data = {
            "time": "2024-12-11 17:27:00+03",
            "duration": 15,
            "periodicity": 3,
            "action": "кофе",
            "is_public": True,
            "place": "home sweet home",
            "reward": "Шоколадка",
            "user": self.user,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_update_habit(self):
        """Тест на изменение данных"""

        data = {
            "place": "Парк",
            "duration": 45,
        }
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, "Парк")
        self.assertEqual(self.habit.duration, 45)

    def test_delete_habit(self):
        """Tест на удаление привычки"""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_list_my_habits(self):
        """Тесты на мои привычки"""
        response = self.client.get(self.my_habits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_public_habits(self):
        """Тесты на публичные привычки"""
        Habit.objects.create(
            user=self.user,
            place="Спортзал",
            time="2024-12-11 17:27:00+03",
            duration=60,
            periodicity=2,
            action="Тренировки",
            started_at="2024-12-11",
            pleasant_habit=True,
            is_public=True,
        )
        response = self.client.get(self.public_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
