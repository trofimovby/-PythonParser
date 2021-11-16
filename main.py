from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
from discord import Webhook, RequestsWebhookAdapter


class Article:
    def __init__(self, text, create_date, href):
        self.create_date = create_date
        self.text = text
        self.href = href


database = {}

url = 'https://www.kufar.by/l/r~minsk/'
webhook_url = "https://discord.com/api/webhooks/"
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
retry_sec = 2


def log_info(message: str):
    while True:
        try:
            webhook.send(message)
            return
        except:
            print(f"No internet connection {datetime.now()}. Retry 10 sec")
            time.sleep(10)


def get_request(url):
    while True:
        try:
            return requests.get(url)
        except ConnectionError as e:
            log_info(f'Cannot get request {datetime.now()}. Retry 10 sec.\nError message: {e}')
        except:
            log_info(f'Cannot get request {datetime.now()}. Retry 10 sec')
        time.sleep(10)


def find_create_date(a):
    createDate = a.find('div')
    return createDate.text


def process_article(article):
    ref = article.find('a')
    article_str = str(ref).lower()
    if "macbook" or "мак" in article_str:
        article_href = ref['href']
        if article_href not in database.keys():
            article_obj = Article(article_str, datetime.now(), article_href)
            find_create_date(ref)
            database[article_href] = article_obj
            log_info(f"Дата добавления: {find_create_date(ref)}\n{article_obj.href}")
            print(f'Найдено новое объявление {article_href}. Найдено в {datetime.now()}')


if __name__ == '__main__':
    while True:
        response = get_request(url)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.findAll('article')
        for article in articles:
            process_article(article)
        print(f'Обработан запрос в {datetime.now()}. Retry {retry_sec} sec')
        time.sleep(retry_sec)
