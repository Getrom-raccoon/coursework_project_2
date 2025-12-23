import json
from abc import ABC, abstractmethod

from src.vacancy import Vacancy


class AbstractFileConnector(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria=None):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(AbstractFileConnector):
    def __init__(self, filename="data/vacancies.json"):
        self.filename = filename
        self._ensure_directory()
        self._ensure_file_exists()

    def _ensure_directory(self):
        """Создаёт папку data, если её нет."""
        import os

        os.makedirs("data", exist_ok=True)

    def _ensure_file_exists(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        vacancies = self.get_vacancies()
        vacancies.append(vacancy)  # ← добавляем объект Vacancy
        self._save_to_file(vacancies)

    def get_vacancies(self, criteria=None):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        vacancies = []
        for item in data:
            vacancy = Vacancy(
                title=item["title"],
                url=item["url"],
                salary=item["salary"],
                description=item["description"],
            )
            vacancies.append(vacancy)

        if criteria:
            filtered = []
            for vac in vacancies:
                match = True
                for key, value in criteria.items():
                    if key == "keyword":
                        if (
                            value.lower() not in vac.title.lower()
                            and value.lower() not in vac.description.lower()
                        ):
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
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v.url != vacancy.url]
        self._save_to_file(vacancies)

    def _save_to_file(self, vacancies):
        with open(self.filename, "w", encoding="utf-8") as f:
            data = [
                {
                    "title": v.title,
                    "url": v.url,
                    "salary": v.salary,
                    "description": v.description,
                }
                for v in vacancies
            ]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def connect_to_db(self):
        pass

    def disconnect_from_db(self):
        pass
