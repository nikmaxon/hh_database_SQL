import csv
import psycopg2

"""Скрипт для заполнения данными таблиц в БД Postgres."""

with psycopg2.connect(
    host="localhost",
    database="north",
    user="postgres",
    password="229"
) as conn:
    with open('north_data\employees_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO employees(first_name, last_name, title, birth_date, notes) VALUES (%s, %s, %s, %s, %s)",
                            (line['first_name'], line['last_name'], line['title'], line['birth_date'], line['notes']))

    with open('north_data\customers_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO customers(customer_id, company_name, contact_name) VALUES (%s, %s, %s)",
                            (line['customer_id'], line['company_name'], line['contact_name']))

    with open('north_data\orders_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO orders(order_id, customer_id, employee_id, order_date, ship_city) VALUES (%s, %s, %s, %s, %s)",
                            (line['order_id'], line['customer_id'], line['employee_id'], line['order_date'], line['ship_city']))

from pprint import pprint

from classes import HeadHunterAPI, SuperJobAPI, Connector


def main():
    vacancies_json = []
    keyword = input('Введите ключевое слово для поиска: ')
    #keyword = 'Python'
    num_pages = input('Введите количество страниц для поиска: ')

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI(keyword)
    superjob_api = SuperJobAPI(keyword)

    for api in (hh_api, superjob_api):
        api.get_vacancies(pages_count=int(num_pages))
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            "1 - вывести список вакансий;\n"
            "exit - для выхода.\n"
        )
        if command.lower() == 'exit':
            break
        elif command == '1':
            vacancies = connector.select()

        for vacancy in vacancies:
            print(vacancy, end='\n\n')


if __name__ == '__main__':
    main()

