import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def test_init_valid(self):
        """Тест инициализации вакансии с корректными данными."""
        vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123", "100 000 руб.", "Требования...")
        self.assertEqual(vacancy.title, "Python Developer")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy.salary, "100 000 руб.")
        self.assertEqual(vacancy.description, "Требования...")

    def test_init_invalid_title(self):
        """Тест инициализации вакансии с пустым названием."""
        with self.assertRaises(ValueError):
            Vacancy("", "https://hh.ru/vacancy/123", "100 000 руб.", "Требования...")

    def test_init_invalid_url(self):
        """Тест инициализации вакансии с некорректной ссылкой."""
        with self.assertRaises(ValueError):
            Vacancy("Python Developer", "not_a_url", "100 000 руб.", "Требования...")

    def test_salary_validation(self):
        """Тест валидации зарплаты."""
        vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123", "", "Требования...")
        self.assertEqual(vacancy.salary, "Зарплата не указана")

    def test_comparison(self):
        """Тест сравнения вакансий по зарплате."""
        v1 = Vacancy("Dev1", "https://example.com/vacancy1", "100000 руб.", "")
        v2 = Vacancy("Dev2", "https://example.com/vacancy2", "150000 руб.", "")
        v3 = Vacancy("Dev3", "https://example.com/vacancy3", "Зарплата не указана", "")

        self.assertTrue(v2 > v1)
        self.assertTrue(v1 > v3)
        self.assertTrue(v3 < v1)

    def test_cast_to_object_list(self):
        """Тест преобразования JSON в список объектов."""
        raw_data = [
            {
                "name": "Python Developer",
                "alternate_url": "https://hh.ru/vacancy/123",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "snippet": {"requirement": "Опыт работы от 3 лет"}
            }
        ]
        vacancies = Vacancy.cast_to_object_list(raw_data)
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0].title, "Python Developer")
        self.assertEqual(vacancies[0].salary, "100000-150000 RUR")


if __name__ == '__main__':
    unittest.main()