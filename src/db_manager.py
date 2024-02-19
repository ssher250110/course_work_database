import psycopg2


class DBManager:
    """
    Класс для работы с базой данных.
    """

    def __init__(self, new_database, exists_database, params):
        """
        Инициализация необходимых параметров.
        :param new_database: Новая база данных.
        :param exists_database: Существующая база данных.
        :param params: Параметры подключения.
        """
        self.params = params
        self.new_database = new_database
        self.exists_database = exists_database

    def create_database(self) -> None:
        """
        Метод создания базы данных.
        """
        conn = psycopg2.connect(dbname=self.exists_database, **self.params)

        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.new_database}")
        cur.execute(f"CREATE DATABASE {self.new_database}")

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        """
        Метод создания таблиц.
        """
        conn = psycopg2.connect(dbname=self.new_database, **self.params)
        with conn.cursor() as cur:
            cur.execute("""DROP TABLE IF EXISTS employers""")
            cur.execute("""CREATE TABLE IF NOT EXISTS employers(
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(100) NOT NULL,
            open_vacancies INTEGER,
            url TEXT
            )
            """)

        with conn.cursor() as cur:
            cur.execute("""DROP TABLE IF EXISTS vacancies""")
            cur.execute("""CREATE TABLE IF NOT EXISTS vacancies(
            id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            vacancy_name VARCHAR(100) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(5),
            url_address TEXT
            )
            """)

        conn.commit()
        conn.close()

    def save_data_to_database(self, data_employers: list[dict], vacancies: list[dict]) -> None:
        """
        Метод заполнения таблиц данными.
        :param data_employers: Данные о компаниях.
        :param vacancies: Данные о вакансиях.
        """
        conn = psycopg2.connect(dbname=self.new_database, **self.params)
        with conn.cursor() as cur:
            for data in data_employers:
                cur.execute("""INSERT INTO employers (employer_id, employer_name, open_vacancies, url)
                            VALUES (%s, %s, %s, %s)""",
                            (data["employer_id"], data["employer_name"], data["open_vacancies"], data["url"]))
            for vacancy in vacancies:
                cur.execute("""INSERT INTO vacancies (employer_id, vacancy_name, salary_from, salary_to, 
                currency, url_address)
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                            (vacancy["employer_id"], vacancy["vacancy_name"], vacancy["salary_from"],
                             vacancy["salary_to"], vacancy["currency"], vacancy["url_address"]))

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Метод получения списка всех компаний и количества вакансий у каждой компании.
        :return:
        """
        conn = psycopg2.connect(dbname=self.new_database, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
            SELECT employer_name, open_vacancies
            FROM employers""")
            response = cur.fetchall()
        return response

    def get_all_vacancies(self) -> list[tuple]:
        """
        Метод получения списка всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки
        на вакансию.
        :return:
        """
        conn = psycopg2.connect(dbname=self.new_database, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
            SELECT employers. employer_name, vacancy_name, salary_from, salary_to, currency, url_address
            FROM vacancies
            JOIN employers USING (employer_id)
            ORDER BY employers. employer_name
            """)
            response = cur.fetchall()
        return response

    def get_avg_salary(self) -> list[tuple]:
        """
        Метод получения средней зарплаты по вакансиям.
        :return:
        """
        conn = psycopg2.connect(dbname=self.new_database, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
            SELECT AVG ((salary_from + salary_to) / 2) FROM vacancies
            """)
            response = cur.fetchall()
        return response

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return:
        """
        conn = psycopg2.connect(dbname=self.new_database, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT employers. employer_name, vacancy_name, salary_from, salary_to, currency
                    FROM vacancies
                    JOIN employers USING (employer_id)
                    WHERE (salary_from + salary_to) / 2 > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies)
                    ORDER BY (salary_from + salary_to) / 2
                    """)
            response = cur.fetchall()
        return response

    def get_vacancies_with_keyword(self, user_word: str) -> list[tuple]:
        """
        Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :return:
        """
        conn = psycopg2.connect(dbname=self.new_database, **self.params)
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT employers. employer_name, vacancy_name, salary_from, salary_to, currency, url_address
                        FROM vacancies
                        JOIN employers USING (employer_id)
                        WHERE Vacancy_name LIKE %s
                        ORDER BY vacancy_name
                            """, (f"%{user_word}%",))
            response = cur.fetchall()
        return response
