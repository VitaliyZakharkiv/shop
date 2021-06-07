import requests
from bs4 import BeautifulSoup as BS

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'accept': '*/*'
}


def url_product(url):
    request = requests.get(url=url)
    return request.text


def get_image(html):
    bs = BS(html, 'html.parser')
    sidebar = bs.find('div', class_='main-media__sidebar')
    link_image = sidebar.find_all('img', class_='thumbnails-slider__image')
    c = 1
    for i in [i.get('data-src') for i in link_image]:
        res = requests.get(url=i, headers=HEADERS)
        with open(f'image/pho/{c}.jpg', 'wb') as file:
            file.write(res.content)
        print(c)
        c += 1


get_image(url_product('https://allo.ua/ua/kompjutery/artline-gaming-x31-x31v08.html'))
