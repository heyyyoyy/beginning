#!/usr/bin/env python3
# -*-coding: utf-8-*-
"""
Скрипт для скачивания фотографий из диалога vk.
"""
import vk
import requests
from datetime import datetime

# Глобальные переменные
USER_LOGIN = input("Введите ваш Login: ")
USER_PASSWORD = input("Введите ваш пароль: ")
PEER_ID = int(input("Введите id пользователя: "))
COUNT = int(input("Количество фотографий: "))


def main():
    """
    Main function
    """
    session = vk.AuthSession(app_id=5852076, user_login=USER_LOGIN,
                             user_password=USER_PASSWORD, scope="messages")

    api = vk.API(session)

    r = api.messages.getHistoryAttachments(
        peer_id=PEER_ID, media_type='photo', count=COUNT)

    x = []
    for i in range(1, COUNT + 1):
        try:
            image = r[str(i)]['photo']['src_big']
            x.append(image)
        except KeyError:
            break

    start = datetime.now()
    for index, i in enumerate(x, start=1):
        resp = requests.get(i)
        with open(i.split('/')[-1], 'wb') as file:
            file.write(resp.content)
        print(index, i.split('/')[-1] + ' downloaded')
    end = datetime.now()
    print('Время скачивания ', end - start)


if __name__ == '__main__':
    main()
