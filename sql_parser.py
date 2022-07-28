from config import *
try:
    from secret_settings import *
except ImportError:
    pass


import pymysql
import json


class SqlManager:

    def __init__(self):
        pass

    @classmethod
    def get_connection(cls):
        connection = pymysql.connect(
            host=host,
            port=port,
            database=db_name,
            user=user,
            password=password,
        )
        return connection

    @classmethod
    def get_teams_records(cls):
        try:
            instance = SqlManager()
            connection = instance.get_connection()
            with connection.cursor() as cursor:
                query = f"SELECT team FROM `teams`"
                cursor.execute(query)
                res = cursor.fetchall()
                """ Список username'ов игроков """
                usernames_list = {}
                for team in res:
                    for data in team:
                        players = []
                        team_name = json.loads(data)['team_name']
                        for value in json.loads(data)['members']:
                            players.append(value['discord'])
                        usernames_list.update({team_name: players})
                return usernames_list
        finally:
            connection.close()