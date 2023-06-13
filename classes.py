import psycopg2


class DBManager:
    def __init__(*params):
        self.connect = psycopg2.connect(*params)

    def