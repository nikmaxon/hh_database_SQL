from pprint import pprint
import pandas as pd
import psycopg2
from hh_parser import HeadHunter


class DBManager:
    def __init__(self, host, database, user, password):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.conn = psycopg2.connect(host=self.host, database="postgres", user=self.user, password=self.password)

    def create_database(self):
        """Создает базу данных в PG"""
        conn = self.conn
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"""DROP DATABASE IF EXISTS {self.database}""")
        cur.execute(f"""CREATE DATABASE {self.database}""")
        conn.close()

    def create_tables(self):
        """Создает таблицы с работодателями и вакансиями"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS employers(
                        company_id int PRIMARY KEY,
                        company_name varchar 
                    )""")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS vacancies(
                        vacancy_id int PRIMARY KEY,
                        vacancy_name varchar,
                        url varchar,
                        salary_from int,
                        salary_to int,
                        company int REFERENCES employers(company_id)
                    )""")
        conn.close()

    def insert_data(self):
        """Заносит информацию в таблицы"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()
        hh = HeadHunter()

        data_employers = hh.get_employers()

        for item in data_employers:
            employers_id = item['id']
            company_name = item['name']
            cur.execute(f"""INSERT INTO employers (company_id, company_name) VALUES ('{employers_id}', '{company_name}') 
                            ON CONFLICT (company_id) DO NOTHING""")

        data_vacancies = hh.get_vacancies()
        for vacancy in data_vacancies:
            vacancy_id = vacancy['id']
            name = vacancy['name']
            url = vacancy['alternate_url']
            salary_from = vacancy['salary']['from']
            salary_to = vacancy['salary']['to']
            company = vacancy['employer']['id']

            cur.execute(f"""INSERT INTO vacancies (vacancy_id, vacancy_name, url, salary_from, salary_to, company) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING""", (vacancy_id, name, url, salary_from, salary_to, company))
        conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""

        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"""SELECT company_name, COUNT(vacancy_name) as vacancies
                        FROM vacancies
                        INNER JOIN employers ON vacancies.company = employers.company_id
                        GROUP BY company_name""")
        result = cur.fetchall()

        df = pd.DataFrame(result, columns=['Название компании', 'Число вакансий'])
        print(df)
        print('-'*100)
        conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на
            вакансию"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"""SELECT company_name, vacancy_name, salary_from, salary_to, url FROM vacancies
INNER JOIN employers ON vacancies.company = employers.company_id""")
        result = cur.fetchall()

        for result in result:
            print(result)
        print('-'*100)
        conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"""SELECT company_name, AVG(salary_from) as avg_salary
                        FROM vacancies
                        INNER JOIN employers ON vacancies.company = employers.company_id
                        GROUP BY company_name""")
        result = cur.fetchall()

        df = pd.DataFrame(result, columns=['Название компании', 'Средняя зарплата'])
        print(df)
        print('-'*100)

        conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"""SELECT vacancy_name, MAX(salary_from) as max_salary
                        FROM vacancies
                        GROUP BY vacancy_name""")
        result = cur.fetchall()

        df = pd.DataFrame(result, columns=['Список вакансий с зарплатой выше средней', 'Зарплата'])
        print(df)
        print('-'*100)

        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например
            “python”"""
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"""SELECT vacancy_name FROM vacancies
                        WHERE vacancy_name LIKE '%{keyword}%'""")
        result = cur.fetchall()

        df = pd.DataFrame(result, columns=[f'Список вакансий со словом "{keyword}"'])
        print(df)
        print('-'*100)

        conn.close()


# db = DBManager(host="localhost", database="headhunter", user="postgres", password="229")
# db.create_database()
# db.create_tables()
# db.insert_data()
# db.get_vacancies_with_keyword('Продавец')
