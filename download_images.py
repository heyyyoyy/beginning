#!/usr/bin/env python3
#-*-coding: utf-8-*-

from bs4 import BeautifulSoup           #Импортируем
import requests                         #необходимые
from datetime import datetime           #библиотеки.


number = int(input("Введите колличество страниц для скачивания картинок: "))    #Вводим число страниц.
url = 'https://alpha.wallhaven.cc/random?page='                                 #Ссылка на сайт.

def get_html(url):                                                      #Создаем функцию
    r = requests.get(url)                                               #возвращающую
    return r.text                                                       #HTML код страницы.

def main():                                                             #Создаем главную функцию.
    start = datetime.now()                                              #Начинаем запись времени скачивания.
    for i in range(1,number+1):                                         #Начало цикла.
        html = get_html(url+str(i))                                     #Получаем HTML код страницы со всеми картинками.
        soup = BeautifulSoup(html, 'lxml')                              #Создаем обЪект soup.
        links = soup.find_all('a', class_='preview')                    #Список со всеми preview ссылками.
        for link in links:                                              #Начало цикла.
            secondary_html = get_html(link['href'])                     #Получаем HTML код страницы с картинкой.
            secondary_soup = BeautifulSoup(secondary_html, 'lxml')      #Создаем обЪект secondary_soup.
            image = secondary_soup.find('img', id='wallpaper')['src']   #Ссылка из атрибута src.
            image = 'https:' + image                                    #Конкатенируем строки.
            resp = requests.get(image)                                  #Забираем наш запрос.
            with open(image[58:], 'wb') as file:                        #Запускаем цикл
                file.write(resp.content)                                #и скачиваем наши картинки.
                print(image[58:], 'скачан')
        end = datetime.now()                                            #Завершаем запись времени.
        print("Время скачивания: " + str(end - start))                  #Выводим время.

if __name__ == '__main__':
    main()