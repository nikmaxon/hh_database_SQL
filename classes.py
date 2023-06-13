import psycopg2
import csv
import psycopg2
from poetry.console.commands import self
import json
import os
from abc import abstractmethod, ABC
from configparser import ParsingError
from pprint import pprint

class AbstractClass(ABC):
    @abstractmethod
    def get_vacancies(self, job_name):
        pass


class HeadHunterAPI(AbstractClass):
    def __init__(self, keyword):
        self.__header = {
            "User-Agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"
        }
        self.__params = {
            "text": keyword,
            "page": 0,
            "per_page": 100
        }
        self.__vacancies = []

    @staticmethod
    def get_salary(salary):
        formatted_salary = [None, None]
        if salary and salary["from"] and salary["from"] != 0:
            formatted_salary[0] = salary["from"] if salary["currency"].lower() == "rur" else salary["from"] * 78
        if salary and salary["to"] and salary["to"] != 0:
            formatted_salary[1] = salary["to"] if salary["currency"].lower() == "rur" else salary["to"] * 78
        return formatted_salary

    def get_request(self):
        response = requests.get('https://api.hh.ru/vacancies/',
                                headers=self.__header,
                                params=self.__params)
        if response.status_code != 200:
            raise ParsingError
        return response.json()['items']

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.__vacancies:
            salary_from, salary_to = self.get_salary(vacancy['salary'])
            formatted_vacancies.append({
                'id': vacancy['id'],
                'title': vacancy['name'],
                'url': vacancy['alternate_url'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'employer': vacancy['employer']['name'],
                'api': 'HeadHunter'
            })
        return formatted_vacancies

    def get_vacancies(self, pages_count=1):
        while self.__params['page'] < pages_count:
            print(f"HeadHunter, Парсинг страницы {self.__params['page'] + 1}", end=": ")
            try:
                values = self.get_request()
            except ParsingError:
                print('Ошибка получения данных')
                break
            print(f"Найдено ({len(values)}) вакансий.")
            self.__vacancies.extend(values)
            self.__params['page'] += 1

class DBManager:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connect = psycopg2.connect(
        host=self.host, #"localhost"
        database=self.database, #"hh"
        user=self.user,#"postgres"
        password=self.password #"229"
    ) as conn:
        with open('north_data\employees_data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for line in reader:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO employees(first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s)",
                                (line['first_name'], line['last_name'], line['title'], line['birth_date'], line['notes']))
    def get_companies_and_vacancies_count():
        """Получает список всех компаний и количество вакансий у каждой компании."""
        pass
    def get_all_vacancies():
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        pass
    def get_avg_salary():
        """получает среднюю зарплату по вакансиям."""
        pass
    def get_vacancies_with_higher_salary():
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass
    def gget_vacancies_with_keyword():
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        pass
