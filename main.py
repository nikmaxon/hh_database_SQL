from hh_parser import HeadHunter
from db_manager import DBManager


#database = input('Введите название базы данных: ')
#password = input('Введите пароль: ')

database = "headhunter"
password = "229"

#Парсинг нанимателей и вакансий с сайта HeadHunter
hh = HeadHunter()
hh.get_employers()
hh.get_vacancies()

#Подключение, создание баз данных, таблиц companies и vacancies
db = DBManager(host="localhost", database=database.lower(), user="postgres", password=password)