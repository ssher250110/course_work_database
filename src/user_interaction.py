import time

from config import config
from src.db_manager import DBManager


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    db_manager = DBManager('database_hh', 'postgres', config())
    while True:
        user_query = input("""
        \rВыберите необходимое действие с данными:
        \r1 - получить список всех компаний и количество вакансий у каждой компании:
        \r2 - получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты
        \rи ссылки на вакансию
        \r3 - получить среднюю зарплату по вакансиям
        \r4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
        \r5 - получить список всех вакансий, в названии которых содержатся переданные в метод слова, например python
        \r0 - выход из программы\n""")

        if user_query == "1":
            list_employers_vacancies = db_manager.get_companies_and_vacancies_count()
            for employers, vacancies in list_employers_vacancies:
                print(f"{(employers.title())} - Количество вакансий: {vacancies}")
            time.sleep(5)

        elif user_query == "2":
            list_all_vacancies = db_manager.get_all_vacancies()
            while True:
                user_count_issue_2 = int(input("Сколько вакансий вывести?\n"
                                               f"Общее кол-во вакансий {len(list_all_vacancies)}\n"))
                if 0 < user_count_issue_2 <= len(list_all_vacancies):
                    for vacancy in list_all_vacancies[:user_count_issue_2]:
                        print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, "
                              f"Зарплата: {vacancy[2]} - {vacancy[3]} {vacancy[4]}, Сайт: {vacancy[5]}")
                    time.sleep(5)
                    break
                else:
                    print("Ошибка ввода количества вакансий")

        elif user_query == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {round(avg_salary[0][0])} RUR")
            time.sleep(3)

        elif user_query == "4":
            higher_salary = db_manager.get_vacancies_with_higher_salary()
            while True:
                user_count_issue_4 = int(input("Сколько вакансий вывести?\n"
                                               f"Общее кол-во вакансий {len(higher_salary)}\n"))
                if 0 < user_count_issue_4 <= len(higher_salary):
                    for salary in higher_salary[:user_count_issue_4]:
                        print(f"Компания: {salary[0]}, Вакансия: {salary[1]}, "
                              f"Зарплата: {salary[2]} - {salary[3]} {salary[4]}")
                    time.sleep(5)
                    break
                else:
                    print("Ошибка ввода количества вакансий")

        elif user_query == "5":
            user_keyword = input("Введите название вакансии для поиска\n").lower()
            keyword = db_manager.get_vacancies_with_keyword(user_keyword)
            if len(keyword) > 0:
                while True:
                    user_count_issue_5 = int(input("Сколько вакансий вывести?\n"
                                                   f"Общее кол-во вакансий {len(keyword)}\n"))
                    if 0 < user_count_issue_5 <= len(keyword):
                        for word in keyword[:user_count_issue_5]:
                            print(f"Компания: {word[0]}, Вакансия: {word[1]}, "
                                  f"Зарплата: {word[2]} - {word[3]} {word[4]}, Сайт: {word[5]}")
                        time.sleep(5)
                        break
                    else:
                        print("Ошибка ввода количества вакансий")
            else:
                print("Данная вакансия отсутствует")
                time.sleep(2)

        elif user_query == "0":
            break

        else:
            print("Ошибка ввода команды. Повторите ввод")
            time.sleep(1)
