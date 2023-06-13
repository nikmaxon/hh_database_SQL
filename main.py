
def main():
    vacancies_json = []
    keyword = input('Введите ключевое слово для поиска: ')
    #keyword = 'Python'
    num_pages = input('Введите количество страниц для поиска: ')

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI(keyword)

    for api in (hh_api):
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

