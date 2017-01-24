#!/usr/bin/env python3

import csv
import requests
from bs4 import BeautifulSoup

base_url = 'http://foxtools.ru/Proxy'

def get_html(url):
    r = requests.get(url)
    return r.text

def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', id='theProxyList')
    projects = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        projects.append({
            'ip': cols[1].text,
            'port': cols[2].text
        })
    return projects


def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    paggination = soup.find('div', class_='pager')
    number = paggination.find_all('a')[-1].text
    return int(number[1:3])


def save(projects):
    with open('proxy.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow('ip:port'.split())
        for project in projects:
            a = project['ip'] + ':' + project['port']
            writer.writerow(a.split())
        print("Файл сохранен.")


def main():
    page_count = get_pages(get_html(base_url))
    print('Всего страниц {}'.format(page_count))

    projects = []

    for page in range(1, page_count+1):
        print('Парсинг %d%%' % (page / page_count * 100))
        projects.extend(parse(get_html(base_url + '?page=%d' % page)))
    save(projects)


if __name__ == '__main__':
    main()
