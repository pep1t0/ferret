# from socket import timeout
# from urllib.request import Request
import requests
import os
import time
import concurrent.futures

# os.system('clear')

FILE_TO_PROCESS = 'subdomains.txt'
DOMAIN_TO_PROCESS = '10.129.18.214'

NUM_WORKERS = 3

def check_subdomain(address, timeout=2):
    try:
        resp = requests.get(address, timeout=timeout)
        
        resp.raise_for_status()
        print('[!] El dominio existe!!!',address, resp, '\n',sep='\t')
    
    except requests.exceptions.HTTPError as err:
        #if err.response.status_code == 404:
        print("[+] Descubierto subdominio:",address)
        
    except requests.exceptions.ConnectionError:
        print('[URL Erronea] No existe',address, sep='\t')
        pass
    except requests.exceptions.Timeout as err:
        print('Excedido el tiempo de espera', address)
    except requests.exceptions.RequestException as err:
        print('Error general', err)
    else:
        print("[+] Descubierto subdominio:",address)
 

def file_fuzz (name_file, domain):
      
    try:
        s = open(name_file,'r')
        content = s.read()
        fuzz_list = content.splitlines()
        
        website_list = [ (f"http://{fuzz}.{domain}") for fuzz in fuzz_list]
        s.close()

        return website_list

    except Exception as exc:
        print('[ERROR] El fichero no se pudo abrir:', os.strerror(exc.errno))

def fura_web(file_p, domain_p):
    
    webby = file_fuzz(file_p, domain_p)
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = {executor.submit(check_subdomain, address,1) for address in webby}
        concurrent.futures.wait(futures)
        
    end_time = time.time()

    print('Tiempo transcurrido: %ssecs',(end_time - start_time))
        
print('INICIO DEL PROCESADO\n')    
fura_web (FILE_TO_PROCESS, DOMAIN_TO_PROCESS)

