import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv


def shorten_link(token, url):
    service_url = 'https://api.vk.ru/method/utils.getShortLink'
    payload = {'v': '5.199', 'access_token': token, 'url': url}
    response = requests.get(service_url, params=payload)
    response.raise_for_status()
    result = response.json()
    if 'error' in result.keys():
        raise requests.exceptions.HTTPError(result['error']['error_msg'])
    return result['response']['short_url']


def count_clicks(token, key):
    service_url = 'https://api.vk.ru/method/utils.getLinkStats'
    payload = {'v': '5.199', 'access_token': token, 'key': key, 'interval': 'forever'}
    response = requests.get(service_url, params=payload)
    response.raise_for_status()
    result = response.json()
    if 'error' in result.keys():
        raise requests.exceptions.HTTPError(result['error']['error_msg'])
    return str(result['response']['stats'][0]['views'])


def is_shorten_link(token, key):
    service_url = 'https://api.vk.ru/method/utils.getLinkStats'
    payload = {'v': '5.199', 'access_token': token, 'key': key, 'interval': 'forever'}
    response = requests.get(service_url, params=payload)
    response.raise_for_status()
    result = response.json()
    return 'error' not in result.keys()


def main():

    load_dotenv()
    token = os.environ['VK_TOKEN']

    url = input('Input URL ')
    parsed_url = urlparse(url)

    if  is_shorten_link(token, parsed_url.path[1:]):
        try:
            print('Количество кликов: {}'.format(count_clicks(token, parsed_url.path[1:])))
        except requests.exceptions.HTTPError:
            print('Вы ввели неправильную ссылку или неверный токен.')
            raise
    else:  
        try:
            print('Сокращенная ссылка: {}'.format(shorten_link(token, url)))
        except requests.exceptions.HTTPError:
            print('Вы ввели неправильную ссылку или неверный токен.')
            raise


if __name__ == '__main__':
    main()
