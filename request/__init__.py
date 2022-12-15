from random import choice
from bs4 import BeautifulSoup
import requests
import argparse


DESCKTOP_AGENTS = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    """
    Возвращает рандомные хедеры для запроса
    """
    return {'User-Agent': choice(DESCKTOP_AGENTS), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def search_href(response, urls: list, url: str) -> list:
    """
    Ищет все ссылки на странице и добавляет их в список для дальнейшего парсинга
    """
    bs = BeautifulSoup(response.text, "lxml")
    temp = bs.find_all("a")  # поиск всех тегов <a> на странице
    for element in temp:  # итерируемся по всем найденым тегам <a>
        href = element.get("href", "")  # вытаскиваем из тега ссылку
        if href[0] == "/":
            href = url + href[1::]  # ссылка на страницу
        else:
            if url in href:
                href = href
        if "#" not in href and href not in urls and "/" in href:
            urls.append(href)

    return urls


def search_form(response) -> int | None:
    """
    Ищет количество форм на странице
    """
    bs = BeautifulSoup(response.text, "lxml")
    temp = bs.find_all("form")
    print(len(temp))
    return len(temp)


def start_parse(args: argparse.Namespace) -> dict:
    """
    Основная функция запуска парсера
    """
    url = args.url
    proxy = args.proxyfile
    if proxy == None:
        proxylist = None
    else:
        with open(proxy) as f:
            proxylist = f.readlines()

    urls = [url]  # список всех ссылок сайта
    i = int()  # для итерации по списку ссылок
    result = dict()

    while i < len(urls):
        url_now = urls[i]

        if proxylist != None:
            proxies = {
                'http': choice(proxylist),
                'https': choice(proxylist)
            }
        else:
            proxies = None
        print(url_now)
        response = requests.get(url_now, headers=random_headers(),
                                proxies=proxies, timeout=1.5)
        if response.status_code != 200:  # проверка статус-кода запроса
            print(response.status_code)
            continue

        # количество форм на странице
        k_forms = search_form(response)
        result[url_now] = k_forms

        search_href(response, urls, url)
        i += 1

    return result
