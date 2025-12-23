import requests
from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def get_vacancies(self, keyword: str) -> list:
        """Получить вакансии по ключевому слову."""
        pass


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с платформой hh.ru."""

    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, keyword: str) -> list:
        """
        Получает вакансии с hh.ru по ключевому слову.
        Возвращает список вакансий в формате JSON.
        """
        params = {
            "text": keyword,
            "area": 1,
            "per_page": 100,
            "page": 0
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except requests.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return []