import vk
from time import sleep


def auth(login, password):
    try:
        session = vk.AuthSession(app_id=5852076, user_login=login, user_password=password, scope='messages')
    except Exception:
        print("Неверно введен пароль.")
    else:
        api_vk = vk.API(session)
        return api_vk


def get_friends(api):
    return api.friends.get(fields='sex')


def send_messege(api, mylist, present):
    for i, friend in enumerate(mylist, start=1):
        if friend['sex'] == 1:
            try:
                api.messages.send(user_id=friend['uid'], message=present)
            except Exception:
                pass
            else:
                print(i, "Сообщение отправлено.")
                sleep(1)


def main():
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    present = input("Введите поздравляшку: ")

    api = auth(login, password)
    friends_list = get_friends(api)

    send_messege(api, friends_list, present)


if __name__ == '__main__':
    main()
