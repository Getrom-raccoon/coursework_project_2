import json
from abc import ABC, abstractmethod


class AbstractFileConnector(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_vacancy(self, vacancy):
        """Добавить вакансию в файл."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria=None):
        """Получить вакансии из файла по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        """Удалить вакансию из файла."""
        pass


class JSONSaver(AbstractFileConnector):
    """Класс для сохранения информации о вакансиях в JSON-файл."""

    def __init__(self, filename="vacancies.json"):
        """
        Инициализация коннектора.
        :param filename: Имя файла для хранения вакансий.
        """
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создает файл, если он не существует."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                json.load(f)
        except FileNotFoundError:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        """
        Добавляет вакансию в JSON-файл.
        :param vacancy: Объект Vacancy.
        """
        vacancies = self.get_vacancies()
        vacancy_dict = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description
        }
        vacancies.append(vacancy_dict)
        self._save_to_file(vacancies)

    def get_vacancies(self, criteria=None):
        """
        Получает вакансии из файла.
        :param criteria: Критерии фильтрации (необязательно).
        :return: Список вакансий (объектов Vacancy).
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
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
                        if value.lower() not in vac.description.lower() and value.lower() not in vac.title.lower():
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

    def delete_vacancy(self, vacancy):
        """
        Удаляет вакансию из файла.
        :param vacancy: Объект Vacancy для удаления.
        """
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v.url != vacancy.url]
        self._save_to_file(vacancies)

    def _save_to_file(self, vacancies):
        """Сохраняет список вакансий в файл."""
        with open(self.filename, 'w', encoding='utf-8') as f:
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

    def connect_to_db(self):
        """Заглушка для подключения к базе данных."""
        pass

    def disconnect_from_db(self):
        """Заглушка для отключения от базы данных."""
        pass