from abc import ABC, abstractmethod

import requests

from settings import HH_URL_EMPLOYERS


class ApiEmployer(ABC):
    """
    Абстрактный класс для получения информации о компаниях через API.
    """

    @abstractmethod
    def get_data_employers(self, company_ids: list[str]) -> list[dict]:
        """
        Абстрактный метод для получения информации о компаниях через API.
        :param company_ids: Список ids компаний.
        :return: Список со словарями с информацией о компаниях.
        """
        raise NotImplementedError


class HHApiEmployer(ApiEmployer):
    """
    Класс для получения информации о компаниях через API.
    """

    def get_data_employers(self, company_ids: list[str]) -> list[dict]:
        """
        Метод для получения информации о компаниях.
        :param company_ids: Список ids компаний.
        :return: Список со словарями с информацией о компаниях.
        """
        data_employers = []
        for company_id in company_ids:
            response_api_hh = requests.get(url=f"{HH_URL_EMPLOYERS}{company_id}").json()
            data_employers.append(response_api_hh)
        return [{"employer_name": data_employer["name"], "open_vacancies": data_employer["open_vacancies"]} for
                data_employer in data_employers]
