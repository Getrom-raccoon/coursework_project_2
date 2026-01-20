import json
from abc import ABC, abstractmethod
from typing import List, Optional

from src.vacancy import Vacancy


class AbstractFileConnector(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавить вакансию в файл.

        :param vacancy: Объект вакансии.
        """
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[dict] = None) -> List[Vacancy]:
        """
        Получить вакансии из файла по критериям.

        :param criteria: Словарь с критериями фильтрации (опционально).
        :return: Список объектов Vacancy.
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удалить вакансию из файла.

        :param vacancy: Объект вакансии для удаления.
        """
        pass


class JSONSaver(AbstractFileConnector):
    """Класс для сохранения информации о вакансиях в JSON-файл."""

    def __init__(self, filename: str = "data/vacancies.json"):
        """
        Инициализация коннектора.

        :param filename: Имя файла для хранения вакансий.
        """
        self.__filename = filename
        self._ensure_directory()
        self._ensure_file_exists()

    @property
    def filename(self) -> str:
        """Публичный геттер для имени файла."""
        return self.__filename

    def _ensure_directory(self) -> None:
        """Создаёт папку data, если её нет."""
        import os
        os.makedirs("data", exist_ok=True)

    def _ensure_file_exists(self) -> None:
        """Создаёт файл, если он не существует."""
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                json.load(f)
        except FileNotFoundError:
            with open(self.__filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в JSON-файл.

        :param vacancy: Объект Vacancy.
        """
        vacancies = self.get_vacancies()
        vacancies.append(vacancy)
        self._save_to_file(vacancies)

    def get_vacancies(self, criteria: Optional[dict] = None) -> List[Vacancy]:
        """
        Получает вакансии из файла.

        :param criteria: Критерии фильтрации (необязательно).
        :return: Список вакансий (объектов Vacancy).
        """
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        vacancies = []
        for item in data:
            vacancy = Vacancy(
                title=item["title"],
                url=item["url"],
                salary=item["salary"],
                description=item["description"]
            )
            vacancies.append(vacancy)

        if criteria:
            filtered = []
            for vac in vacancies:
                match = True
                for key, value in criteria.items():
                    if key == "keyword":
                        if value.lower() not in vac.title.lower() and value.lower() not in vac.description.lower():
                            match = False
                            break
                    elif key == "salary_min":
                        if vac._get_salary_value() < value:
                            match = False
                            break
                if match:
                    filtered.append(vac)
            return filtered

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из файла.

        :param vacancy: Объект Vacancy для удаления.
        """
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v.url != vacancy.url]
        self._save_to_file(vacancies)

    def _save_to_file(self, vacancies: List[Vacancy]) -> None:
        """Сохраняет список вакансий в файл."""
        with open(self.__filename, 'w', encoding='utf-8') as f:
            data = [
                {
                    "title": v.title,
                    "url": v.url,
                    "salary": v.salary,
                    "description": v.description
                }
                for v in vacancies
            ]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def connect_to_db(self) -> None:
        """Заглушка для подключения к базе данных."""
        pass

    def disconnect_from_db(self) -> None:
        """Заглушка для отключения от базы данных."""
        pass
