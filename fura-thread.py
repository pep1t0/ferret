# from socket import timeout
# from urllib.request import Request
import requests
import os
import time
import concurrent.futures


os.system('cls')

WEBSITE_LIST = [
    'https://envato.com',
    'http://amazon.co.uk',
    'http://amazon.com',
    'http://facebook.com',
    'http://google.com',
    'http://google.fr',
    'http://google.es',
    'http://google.co.uk',
    'http://internet.org',
    'http://gmail.com',
    'http://stackoverflow.com',
    'http://github.com',
    'http://heroku.com',
    'http://really-cool-available-domain.com',
    'http://djangoproject.com',
    'http://rubyonrails.org',
    'http://basecamp.com',
    'http://trello.com',
    'http://yiiframework.com',
    'http://shopify.com',
    'http://another-really-interesting-domain.co',
    'http://airbnb.com',
    'http://instagram.com',
    'http://snapchat.com',
    'http://youtube.com',
    'http://baidu.com',
    'http://yahoo.com',
    'http://live.com',
    'http://linkedin.com',
    'http://yandex.ru',
    'http://netflix.com',
    'http://wordpress.com',
    'http://bing.com',
]

NUM_WORKERS = 5

def check_subdomain(address, timeout=2):
    try:
        resp = requests.head(address, timeout=2)
        resp.raise_for_status()
        print('El dominio existe',address,resp,sep='')

    except requests.exceptions.HTTPError as err:
        print('[HTTPError]',err)
    except requests.exceptions.ConnectionError as err:
        print('[URL Erronea]',address, 'El dominio no existe',err,sep='')
    except requests.exceptions.Timeout as err:
        print('Excedido el tiempo de espera',err)
    except requests.exceptions.RequestException as err:
        print('Error general',err)

print('START PoC')
start_time = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    futures = {executor.submit(check_subdomain, address) for address in WEBSITE_LIST}
    concurrent.futures.wait(futures)

end_time = time.time()

print('Tiempo transcurrido: %ssecs',(end_time - start_time))