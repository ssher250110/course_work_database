from config import config
from settings import company_ids
from src.db_manager import DBManager
from src.work_api_employers import HHApiEmployer
from src.work_api_vacancies import HHApiVacancies


def data_database() -> None:
    """
    Функция для работы с API HeadHunter, создания базы данных и таблиц, и заполнения таблиц данными.
    """
    api_employers = HHApiEmployer()
    get_employers = api_employers.get_data_employers(company_ids)

    api_vacancies = HHApiVacancies()
    api = api_vacancies.get_vacancies(company_ids)

    db_manager = DBManager('database_hh', 'postgres', config())

    db_manager.create_database()
    db_manager.create_tables()
    db_manager.save_data_to_database(get_employers, api)
