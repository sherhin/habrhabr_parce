
import requests
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import csv


def get_html(url):  # получение содержимого страницы
    try:
        response = requests.get(
            url, headers={'User-Agent': FakeUserAgent().chrome})
        response.raise_for_status()
        html = response.content
        return html
    except (requests.RequestException, ValueError):
        print('Что-то пошло не так')
        return False


def get_yearly_top(count):  # получаем желаемое количество статей
    html = get_html('https://habr.com/ru/top/yearly/')
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.findAll('article')
    for item in range(count):
        post = posts[item]
        author = post.find(
            'span', class_="user-info__nickname user-info__nickname_small", text=True).text
        date = post.find('span', class_="post__time").text
        title = post.find('a', class_="post__title_link").text
        short_text = post.find('div').text
        article_info = [title, date, author, short_text]
        with open('habrhabr_data.csv', 'a', encoding='utf8', newline='') as output:
            f = csv.writer(output, delimiter=';')
            f.writerow(article_info)


if __name__ == "__main__":
    get_yearly_top(3)
