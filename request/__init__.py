from random import choice
from bs4 import BeautifulSoup
import requests
import settings


DESCTOP_AGENTS = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

proxies = {
    'http': choice(settings.PROXIES),
    'https': choice(settings.PROXIES)
}


def random_headers():
    """
    Возвращает рандомные хедеры для запроса
    """
    return {'User-Agent': choice(DESCTOP_AGENTS), 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def search_href(url: str, urls: list) -> list:
    """
    Ищет все ссылки на странице и добавляет их в список для дальнейшего парсинга
    """
    response = requests.get(url, headers=random_headers(),
                            proxies=proxies, timeout=1.5)
    if response.status_code != 200:  # проверка статус-кода запроса
        print(response.status_code)
        return urls

    bs = BeautifulSoup(response.text, "lxml")
    temp = bs.find_all("a")  # поиск всех тегов <a> на странице
    for element in temp:  # итерируемся по всем найденым тегам <a>
        href = element.get("href", "")  # вытаскиваем из тега ссылку
        if "#" not in href and href not in urls and "/" in href:
            urls.append(href)

    return urls


def search_form(url: str) -> int | None:
    """
    Ищет количество форм на странице
    """
    print(url)
    response = requests.get(url, headers=random_headers(),
                            proxies=proxies, timeout=1.5)
    if response.status_code != 200:  # проверка статус-кода запроса
        print("None: ", response.status_code)
        return None

    bs = BeautifulSoup(response.text, "lxml")
    temp = bs.find_all("form")
    print(len(temp))
    return len(temp)


def start_parse(url: str) -> dict:
    """
    Основная функция запуска парсера
    """
    urls = list()  # список всех ссылок сайта
    i = int()  # для итерации по списку ссылок
    result = dict()

    search_href(url, urls)
    # print(urls)
    while i < len(urls):
        # print(urls[i])
        if urls[i][0] == "/":
            url_now = url + urls[i][1:]  # ссылка на страницу
        else:
            if url in urls[i]:
                url_now = urls[i]
            else:
                i += 1
                continue

        k_forms = search_form(url_now)  # количество форм на странице
        result[url_now] = k_forms

        search_href(url_now, urls)
        i += 1

    return result
