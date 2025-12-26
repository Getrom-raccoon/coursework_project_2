

class Vacancy:
    """Класс для представления вакансии."""

    def __init__(self, title: str, url: str, salary: str, description: str):
        """
        Инициализация вакансии.
        :param title: Название вакансии
        :param url: Ссылка на вакансию
        :param salary: Зарплата (строка)
        :param description: Описание вакансии
        """
        self.__title = self._validate_title(title)
        self.__url = self._validate_url(url)
        self.__salary = self._validate_salary(salary)
        self.__description = description or ""

    @property
    def title(self):
        """Публичный геттер для title."""
        return self.__title

    @property
    def url(self):
        """Публичный геттер для url."""
        return self.__url

    @property
    def salary(self):
        """Публичный геттер для salary."""
        return self.__salary

    @property
    def description(self):
        """Публичный геттер для description."""
        return self.__description

    def _validate_title(self, title: str) -> str:
        """Валидация названия вакансии."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название вакансии не может быть пустым.")
        return title.strip()

    def _validate_url(self, url: str) -> str:
        """Валидация ссылки."""
        if not isinstance(url, str) or not url.startswith("http"):
            raise ValueError("Некорректная ссылка на вакансию.")
        return url

    def _validate_salary(self, salary: str) -> str:
        """Валидация зарплаты."""
        if not isinstance(salary, str):
            salary = ""
        if not salary.strip():
            return "Зарплата не указана"
        return salary.strip()

    def __lt__(self, other):
        """Метод для сравнения вакансий по зарплате (меньше)."""
        return self._get_salary_value() < other._get_salary_value()

    def __gt__(self, other):
        """Метод для сравнения вакансий по зарплате (больше)."""
        return self._get_salary_value() > other._get_salary_value()

    def __eq__(self, other):
        """Метод для сравнения вакансий по зарплате (равно)."""
        return self._get_salary_value() == other._get_salary_value()

    def _get_salary_value(self) -> int:
        """
        Вспомогательный метод для получения числового значения зарплаты.
        Если зарплата не указана или не может быть преобразована, возвращает 0.
        """
        if "Зарплата не указана" in self.salary:
            return 0

        # Упрощенная логика: берем нижнюю границу диапазона
        try:
            # Убираем пробелы и символы, оставляем только цифры
            clean_salary = "".join(filter(str.isdigit, self.salary))
            if clean_salary:
                return int(clean_salary)
        except (ValueError, TypeError):
            pass
        return 0

    def __str__(self):
        """Строковое представление вакансии."""
        return f"{self.title}\n{self.url}\n{self.salary}\n{self.description[:100]}..."

    @classmethod
    def cast_to_object_list(cls, vacancies_json: list) -> list:
        """
        Преобразует список вакансий из JSON в список объектов Vacancy.
        :param vacancies_json: Список вакансий в формате JSON.
        :return: Список объектов Vacancy.
        """
        vacancies = []
        for item in vacancies_json:
            title = item.get("name", "")
            url = item.get("alternate_url", "")
            salary_info = item.get("salary", {})
            if salary_info:
                from_salary = salary_info.get("from")
                to_salary = salary_info.get("to")
                currency = salary_info.get("currency", "")
                if from_salary and to_salary:
                    salary_str = f"{from_salary}-{to_salary} {currency}"
                elif from_salary:
                    salary_str = f"От {from_salary} {currency}"
                elif to_salary:
                    salary_str = f"До {to_salary} {currency}"
                else:
                    salary_str = "Зарплата не указана"
            else:
                salary_str = "Зарплата не указана"
            description = item.get("snippet", {}).get("requirement", "") or ""
            vacancy = cls(title, url, salary_str, description)
            vacancies.append(vacancy)
        return vacancies
