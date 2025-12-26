from src.vacancy import Vacancy


def filter_vacancies(vacancies: list[Vacancy], keywords: list[str]) -> list[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам.
    :param vacancies: Список вакансий.
    :param keywords: Список ключевых слов.
    :return: Отфильтрованный список вакансий.
    """
    if not keywords:
        return vacancies
    filtered = []
    for vacancy in vacancies:
        for word in keywords:
            if word.lower() in vacancy.title.lower() or word.lower() in vacancy.description.lower():
                filtered.append(vacancy)
                break
    return filtered


def get_vacancies_by_salary(vacancies: list[Vacancy], salary_range_str: str) -> list[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат.
    :param vacancies: Список вакансий.
    :param salary_range_str: Строка диапазона зарплат (например, "100000 - 150000").
    :return: Отфильтрованный список вакансий.
    """
    try:
        parts = salary_range_str.split('-')
        if len(parts) == 2:
            min_salary = int(parts[0].strip())
            max_salary = int(parts[1].strip())
            return [v for v in vacancies if min_salary <= v._get_salary_value() <= max_salary]
        else:
            min_salary = int(salary_range_str.strip())
            return [v for v in vacancies if v._get_salary_value() >= min_salary]
    except (ValueError, AttributeError):
        return vacancies


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    """
    Сортирует вакансии по зарплате (по убыванию).
    :param vacancies: Список вакансий.
    :return: Отсортированный список.
    """
    return sorted(vacancies, key=lambda x: x._get_salary_value(), reverse=True)


def get_top_vacancies(vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    """
    Возвращает топ N вакансий.
    :param vacancies: Список вакансий.
    :param top_n: Количество вакансий для вывода.
    :return: Список топ N вакансий.
    """
    return vacancies[:top_n]


def print_vacancies(vacancies: list[Vacancy]):
    """
    Выводит вакансии в консоль.
    :param vacancies: Список вакансий.
    """
    if not vacancies:
        print("Вакансий не найдено.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{i}. {vacancy.title}")
        print(f"   Ссылка: {vacancy.url}")
        print(f"   Зарплата: {vacancy.salary}")
        print(f"   Описание: {vacancy.description[:200]}...")