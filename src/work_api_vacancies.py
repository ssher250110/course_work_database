import time
from abc import ABC, abstractmethod
from typing import Any

import requests

from settings import HH_URL_VACANCIES


class ApiVacancies(ABC):
    """
    Абстрактный класс для получения вакансии через API
    """

    @abstractmethod
    def get_vacancies(self, company_ids: list[str]) -> list[dict]:
        """
        Абстрактный метод для получения вакансий
        :return: список вакансий в виде словарей
        """
        raise NotImplementedError


class HHApiVacancies(ApiVacancies):
    """
    Класс для получения вакансии через API
    """

    def get_vacancies(self, company_ids: list[str]) -> list[dict]:
        """
        Метод для получения информации о вакансиях компаний
        :param company_ids: список id компаний
        :return: список со словарями информации о вакансиях компаний
        """
        data = []
        data_vacancies = []
        for company_id in company_ids:
            page = 0
            count_pages = requests.get(url=f"{HH_URL_VACANCIES}{company_id}", params={"per_page": 100}).json()["pages"]
            time.sleep(1)
            while page < count_pages:
                response = requests.get(url=f"{HH_URL_VACANCIES}{company_id}", params={"per_page": 100}).json()["items"]
                data_vacancies.extend(response)
                page += 1
            data.extend(data_vacancies)
        return [{"employer_id": int(data_vacancy["employer"]["id"]),
                 "vacancy_name": data_vacancy["name"].lower(),
                 "salary_from": [data_vacancy["salary"]["from"] if data_vacancy.get("salary") else None][0],
                 "salary_to": [data_vacancy["salary"]["to"] if data_vacancy.get("salary") else None][0],
                 "currency": [data_vacancy["salary"]["currency"] if data_vacancy.get("salary") else None][0],
                 "url_address": data_vacancy["alternate_url"]} for data_vacancy in data]
