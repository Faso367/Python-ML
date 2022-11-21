import requests
from bs4 import BeautifulSoup


def search_href(url: str, urls: list) -> list:
    """
    Ищет все ссылки на странице и добавляет их в список для дальнейшего парсинга
    """
    response = requests.get(url)
    if response.status_code != 200:  # проверка статус-кода запроса
        return urls

    bs = BeautifulSoup(response.text, "lxml")
    temp = bs.find_all("a")  # поиск всех тегов <a> на странице
    for element in temp:  # итерируемся по всем найденым тегам <a>
        href = element.get("href", "")  # вытаскиваем из тега ссылку
        if href != "#" and href not in urls:
            urls.append(href)

    return urls


def main():
    url = input("url address: ")
    urls = search_href(url, [])
    print(urls)


if __name__ == "__main__":
    main()
