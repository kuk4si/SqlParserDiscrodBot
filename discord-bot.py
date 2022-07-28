from config import BOT_TOKEN, SECRET_KEY
try:
    from secret_settings import BOT_TOKEN, SECRET_KEY
except ImportError:
    pass

import time
import discord
from sql_parser import SqlManager


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        """ Проверка на отправителя """
        if message.author != client.user:

            """ Проверка на валидность префиксв и ключа """
            if str(message.content).split(' ')[0] == '>>' and str(message.content).split(' ')[1] != SECRET_KEY:
                await message.reply('Неверный ключ!')

            if str(message.content).split(' ')[0] == '>>' and str(message.content).split(' ')[1] == SECRET_KEY:

                """
                    all - извлекает из БД команды и дискорды игроков, возвращает 
                    1) !at TEA_NAME
                    2) !am {player_discord} {player_discord} {player_discord} {player_discord} {player_discord}
                """

                if str(message.content).split(' ')[2] == "all":
                    sql_manager = SqlManager()
                    res = sql_manager.get_teams_records()
                    if res:
                        for team_name, discords in res.items():
                            await message.reply(f"!at {team_name}")
                            players_string = "!am"
                            for player in discords:
                                players_string += f' {player}'
                            await message.reply(players_string)
                            time.sleep(2)


""" Bot start """
if __name__ == '__main__':
    client = MyClient()
    client.run(BOT_TOKEN)
