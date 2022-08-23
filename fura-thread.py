# from socket import timeout
# from urllib.request import Request
import requests
import os
import time
import concurrent.futures


os.system('cls')

WEBLIST = [
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
        print('Direccion:', address)
        resp = requests.head(address, timeout=timeout)
        resp.raise_for_status()
        print('El dominio existe',address, resp, '\n',sep=' ')
    except requests.exceptions.HTTPError as err:
        print('[HTTPError]', address)
    except requests.exceptions.ConnectionError as err:
        print('[URL Erronea] No existe',address, sep='')
    except requests.exceptions.Timeout as err:
        print('Excedido el tiempo de espera', address)
    except requests.exceptions.RequestException as err:
        print('Error general', err)
 

def file_fuzz (name_file, domain):
      
    try:
        s = open(name_file,'r')
        fuzz_list = s.readlines()
        fuzz_list = [line.rstrip('\n') for line in fuzz_list] # Eliminamos el retorno de carro \n que se añade en linux con readlines

        website_list = [('http://' + fuzz + '.' + domain) for fuzz in fuzz_list]
        s.close()

        return website_list

    except Exception as exc:
        print('[ERROR] El fichero no se pudo abrir:', os.strerror(exc.errno))

def fura_web():
    
    webby = file_fuzz('subdomains.txt','google.es')
    print('START PoC')
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = {executor.submit(check_subdomain, address,1) for address in webby}
        concurrent.futures.wait(futures)
        
    end_time = time.time()

    print('Tiempo transcurrido: %ssecs',(end_time - start_time))
        
    


fura_web()

