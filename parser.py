import requests
from bs4 import BeautifulSoup
import pprint


URL = 'https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text=Python+junior&from=suggest_post'
HEADERS = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/84.0.4147.86 YaBrowser/20.8.0.894 Yowser/2.5 Yptp/1.23 Safari/537.36',
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,'
    'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'vacancy-serp-item')


    vacancies = []
    for item in items:
        salary = item.find('div', class_='vacancy-serp-item__sidebar')
        if salary:
            salary = salary.get_text().replace('\xa0', '')
        else:
            salary = 'Зарплата не указана'

        vacancies.append({
        'title' : item.find('div', class_ = 'vacancy-serp-item__info').get_text(),
        'link': item.find('a', class_='bloko-link HH-LinkModifier').get('href'),
        'employer': item.find('div', class_='vacancy-serp-item__meta-info').get_text().replace('\xa0', ''),
        'salary': salary,
        })

    return vacancies


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        vacancies = get_content(html.text)
        print(vacancies)
    else:
        print('Ошибка соединения с сайтом')

parse()