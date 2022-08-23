# from socket import timeout
# from urllib.request import Request
import requests
import os
import time
import concurrent.futures

os.system('clear')

FILE_TO_PROCESS = 'subdomains.txt'
DOMAIN_TO_PROCESS = 'thetoppers.htb'

NUM_WORKERS = 5

def check_subdomain(address, timeout=2):
    try:
        resp = requests.get(address, timeout=timeout)
        resp.raise_for_status()
        print('[EXISTE] El dominio existe!!!',address, resp, '\n',sep='\t')
    except requests.exceptions.HTTPError as err:
        print('[HTTPError]', address)
    except requests.exceptions.ConnectionError as err:
        print('[URL Erronea] No existe',address, sep='\t')
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
    
    webby = file_fuzz(FILE_TO_PROCESS, DOMAIN_TO_PROCESS)
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = {executor.submit(check_subdomain, address,1) for address in webby}
        concurrent.futures.wait(futures)
        
    end_time = time.time()

    print('Tiempo transcurrido: %ssecs',(end_time - start_time))
        
print('INICIO DEL PROCESADO\n')    
fura_web()

