import psycopg2

from config import config
from settings import company_ids
from src.db_manager import DBManager
from src.work_api_employers import HHApiEmployer
from src.work_api_vacancies import HHApiVacancies
from user_exceptions import ApiError, ConnectError


def load_data_employers():
    """
    Функция для загрузки данных о компаниях с HeadHunter.
    """
    api_employers = HHApiEmployer()

    get_employers = []
    try:
        get_employers = api_employers.get_data_employers(company_ids)
    except ApiError:
        print("Ошибка получения данных с HeadHunter")
    return get_employers


def load_data_vacancies():
    """
    Функция для загрузки данных о вакансиях с HeadHunter.
    """
    api_vacancies = HHApiVacancies()
    api = []
    try:
        api = api_vacancies.get_vacancies(company_ids)
    except ApiError:
        print("Ошибка получения данных с HeadHunter")
    return api


def load_data_database():
    """
    Функция создания базы данных и таблиц, и заполнения таблиц данными.
    """
    db_manager = DBManager('database_hh', 'postgres', config())
    try:
        db_manager.create_database()
    except ConnectError:
        print("Ошибка подключения к базе данных")

    db_manager.create_tables()
    db_manager.save_data_to_database(load_data_employers(), load_data_vacancies())
