import psycopg2


class DBManager:
    """
    Класс для работы с базой данных.
    """

    def __init__(self, database_name, params):
        """
        Инициализация необходимых параметров
        :param database_name: имя новой базы данных
        :param params: параметры подключения
        """
        self.params = params
        self.database_name = database_name

    def create_database(self) -> None:
        """
        Метод создания базы данных.
        """
        conn = psycopg2.connect(dbname="postgres", **self.params)

        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        cur.close()
        conn.close()

    def create_tables(self) -> None:
        """
        Метод создания таблиц.
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS employers(
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(100) NOT NULL,
            open_vacancies INTEGER,
            url TEXT
            )
            """)

        with conn.cursor() as cur:
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
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
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
