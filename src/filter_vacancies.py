from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_connector import JSONSaver


def filter_vacancies(vacancies, keywords):
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


def get_vacancies_by_salary(vacancies, salary_range_str):
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


def sort_vacancies(vacancies):
    """
    Сортирует вакансии по зарплате (по убыванию).
    :param vacancies: Список вакансий.
    :return: Отсортированный список.
    """
    return sorted(vacancies, key=lambda x: x._get_salary_value(), reverse=True)


def get_top_vacancies(vacancies, top_n):
    """
    Возвращает топ N вакансий.
    :param vacancies: Список вакансий.
    :param top_n: Количество вакансий для вывода.
    :return: Список топ N вакансий.
    """
    return vacancies[:top_n]


def print_vacancies(vacancies):
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


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль.
    """
    print("=== Поиск вакансий на hh.ru ===")

    platforms = ["HeadHunter"]
    print("Доступные платформы:")
    for i, platform in enumerate(platforms, 1):
        print(f"{i}. {platform}")

    choice = input("Выберите платформу (по умолчанию 1): ").strip()
    if choice == "2":
        print("Пока доступна только HeadHunter.")
        return

    search_query = input("Введите поисковый запрос: ").strip()
    if not search_query:
        print("Поисковый запрос не может быть пустым.")
        return

    hh_api = HeadHunterAPI()
    raw_vacancies = hh_api.get_vacancies(search_query)
    if not raw_vacancies:
        print("Не удалось получить вакансии с hh.ru.")
        return

    vacancies_list = Vacancy.cast_to_object_list(raw_vacancies)
    print(f"Получено {len(vacancies_list)} вакансий.")

    json_saver = JSONSaver()
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)
    print(f"Вакансии сохранены в файл {json_saver.filename}.")

    top_n = int(input("Введите количество вакансий для вывода в топ N: ") or 5)
    filter_words_input = input("Введите ключевые слова для фильтрации вакансий (через пробел): ")
    filter_words = filter_words_input.split() if filter_words_input else []
    salary_range = input("Введите диапазон зарплат (например, 100000 - 150000): ").strip()

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    if salary_range:
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    else:
        ranged_vacancies = filtered_vacancies
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print(f"\n=== Топ {top_n} вакансий по зарплате ===")
    print_vacancies(top_vacancies)