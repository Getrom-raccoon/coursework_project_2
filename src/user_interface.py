from src.api import HeadHunterAPI
from src.file_connector import JSONSaver
from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, print_vacancies,
                       sort_vacancies)
from src.vacancy import Vacancy


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
    filter_words_input = input(
        "Введите ключевые слова для фильтрации вакансий (через пробел): "
    )
    filter_words = filter_words_input.split() if filter_words_input else []
    salary_range = input(
        "Введите диапазон зарплат (например, 100000 - 150000): "
    ).strip()

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    if salary_range:
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    else:
        ranged_vacancies = filtered_vacancies
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print(f"\n=== Топ {top_n} вакансий по зарплате ===")
    print_vacancies(top_vacancies)
