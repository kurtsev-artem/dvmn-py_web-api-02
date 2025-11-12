
import requests
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

def shorten_link(token, url):
    service_url = 'https://api.vk.ru/method/utils.getShortLink'
    payload = {'v':'5.199', 'access_token': token,'url':url}
    response = requests.get(service_url,params=payload)
    response.raise_for_status()
    if 'error' in response.json().keys():
        return (response.json()['error']['error_msg'])
     return 'Сокращенная ссылка: ' + (response.json()['response']['short_url'])

def count_clicks(token, key):
    service_url = 'https://api.vk.ru/method/utils.getLinkStats'
    payload = {'v':'5.199', 'access_token': token,'key':key,'interval':'forever'}
    response = requests.get(service_url,params=payload)
    response.raise_for_status()
    if 'error' in response.json().keys():
        return (response.json()['error']['error_msg'])
    return 'Количество кликов: ' + str(response.json()['response']['stats'][0]['views'])

def is_shorten_link(url):
    parsed = urlparse(url)
    if (parsed.netloc == 'vk.cc'):
        return True
    else:
        return False

def main():

    load_dotenv()
    token = os.getenv('VK_TOKEN')
    
    url =   input('Input URL ')
 
    if (not is_shorten_link(url)):

        try:
            print (shorten_link(token, url))
        except requests.exceptions.HTTPError:
            print('HTTPError')
    else:
        parsed = urlparse(url)
        try:
            print(count_clicks(token, parsed.path[1:]))
        except requests.exceptions.HTTPError:
            print('HTTPError')

if __name__ == '__main__':
    main()    
