# _*_coding: utf-8_*_

import vk
import sys
from datetime import datetime
import time
from networkx import cubical_graph, spring_layout, draw
import pylab as plt

# Константы
LOGIN = input('Введите ваш Login: ')
PASSWORD = input('Введите ваш пароль: ')


def authorization(login, password):
    """Авторизация вк"""
    try:
        session = vk.AuthSession(app_id='5852076', user_login=LOGIN,
                                 user_password=PASSWORD, scope='friends')
    except Exception:
        # Если неправильно введен пароль или логин
        sys.exit()
    else:
        api = vk.API(session)
    return api


def get_friends(api):
    """Функция возвращает список друзей"""
    print('Начинаем собирать информацию ваших друзей')
    my_friends = api.friends.get(fields='uid,first_name,last_name,photo')
    print('У вас', len(my_friends), 'друзей')
    return my_friends


def get_users(api, mutual_friends):
    """Получаем информацию об общих друзьях"""
    friends_mutual = api.users.get(user_ids=mutual_friends, fields='photo')
    return friends_mutual


def get_mutual(api, my_friends):
    """Собирает id общих друзей"""
    xlist = []
    for index, my_friend in enumerate(my_friends, start=1):
        try:
            mutual_friends = api.friends.getMutual(target_uid=my_friend['uid'])
        except Exception:
            print(index, my_friend['first_name'] + ' ' + my_friend['last_name'] + ' удален(а)')
        else:
            # Вызываем функцию для сбора подробной информации
            friends_mutual = get_users(api, mutual_friends)
            time.sleep(0.7)
            xlist.append((my_friend, friends_mutual))
            print(index, my_friend['first_name'] + ' ' + my_friend['last_name'] + ' добавлен(а) в список')
    return xlist


def get_nodes_edges(xlist):
    """Получаем наши вершины и ребра"""
    nodes = []
    lst = []

    for i in xlist:
        # Вызываем функцию для добавления вершин и ребер в словарь
        update(i, nodes, lst)
    return nodes, lst


def update(i, nodes, lst):
    """Добавляем вершины и ребер"""
    global uid
    for j in i:
        if j == i[0]:
            uid = j['uid']
            nodes.append(uid)
        else:
            for value in j:
                lst.append((uid, value['uid']))


def make_graph(nodes, lst):
    """Построение графа"""
    print('Начинаем строить граф')

    graph = cubical_graph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(lst)
    draw(graph, pos=spring_layout(graph), node_size=150)
    name = input('Введите имя файла: ')
    plt.savefig(name + '.png')
    plt.close()


def main():
    """Main function"""
    start = datetime.now()

    api = authorization(LOGIN, PASSWORD)
    my_friends = get_friends(api)
    xlist = get_mutual(api, my_friends)
    nodes, edges = get_nodes_edges(xlist)
    make_graph(nodes, edges)

    end = datetime.now()
    print('Время выполения', end - start)


if __name__ == '__main__':
    main()
