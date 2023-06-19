from pprint import pprint

import requests


class HeadHunter():
    def __init__(self):
        self.employers_id = [int(elem['id']) for elem in self.get_employers()]

    def get_employers(self):
        response = requests.get('https://api.hh.ru/employers',
                                {'per_page': 10, 'area': 113, 'only_with_vacancies': True}).json()
        return response['items']

    def get_vacancies(self):
        vacancies = []
        for id in self.employers_id:
            response = requests.get('https://api.hh.ru/vacancies', {'employer_id': id, 'per_page': 10}).json()['items']
            vacancies.extend(response)
        return vacancies
