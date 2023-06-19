from db_manager import DBManager
from hh_parser import HeadHunter


database = input('Введите название для базы данных: ')
password = input('Введите пароль: ')

#Подключение, создание баз данных, таблиц companies и vacancies
db = DBManager(host="localhost", database=database.lower(), user="postgres", password=password)
db.create_database()
db.create_tables()
db.insert_data()

while True:
    command = input(
        "1 - Cписок всех компаний и количество вакансий у каждой компании;\n"
        "2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию;\n"
        "3 - Cредняя зарплата по вакансиям;\n"
        "4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям;\n"
        "5 - Список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”;\n"
        "exit - для выхода.\n"
    )
    if command.lower() == 'exit':
        break
    elif command == '1':
        db.get_companies_and_vacancies_count()
    elif command == '2':
        db.get_all_vacancies()
    elif command == '3':
        db.get_avg_salary()
    elif command == '4':
        db.get_vacancies_with_higher_salary()
    elif command == '5':
        keyword = input('Введите слово: ')
        db.get_vacancies_with_keyword(keyword.title())
    else:
        break

