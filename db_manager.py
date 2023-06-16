from pprint import pprint

import psycopg2
from hh_parser import HeadHunter


class DBManager:
    def __init__(self, host, database, user, password):
        self.database = database
        self.user = user
        self.password = password
        self.host = host

    def create_database(self):
        conn = psycopg2.connect(host=self.host, database="postgres", user=self.user, password=self.password)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"""DROP DATABASE IF EXISTS {self.database}""")
        cur.execute(f"""CREATE DATABASE {self.database}""")
        conn.close()

    def create_tables(self):
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


#db = DBManager("localhost", "headhunter", "postgres", "229")
db = DBManager(host="localhost", database="headhunter", user="postgres", password="229")
db.create_database()
db.create_tables()
db.insert_data()

