from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import datetime

# Requisitando página inicial
options = Options()
# options.add_argument('--headless')
options.add_argument('window-size=400,600')
links= []
lista_reclamacoes = []
url_base = 'https://www.reclameaqui.com.br'
errorlist = []

def ultima_pag():
    navegador = webdriver.Chrome(options=options)
    sleep(1)
    navegador.get('https://www.reclameaqui.com.br/empresa/sou-energy/lista-reclamacoes/')
    sleep(1)
    s = BeautifulSoup(navegador.page_source, 'html.parser')
    ult_pag = s.find('div', class_='sc-1sm4sxr-3 eejODo').find('ul', class_='sc-jhGUec eGyFMq').find_all('li')
    ult_pag = int(ult_pag[-2].text)
    return ult_pag

def main(x):
    url = f'https://www.reclameaqui.com.br/empresa/sou-energy/lista-reclamacoes/?pagina={x}' 
    links = []
    # Pegando os dados do site e todas as reclamacoes da pagina
    navegador = webdriver.Chrome(options=options)
    sleep(2)
    navegador.get(url)
    sleep(2)
    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser')
    
   
    urls = site.findAll('div', attrs={'class': 'sc-1pe7b5t-0 bJdtis'}) # Conjunto com LINKS da pag

    for i in urls:
        link_req = url_base +i.find('a')['href']
        links.append(link_req)
    print(links)    
    
    for link in links:
        sleep(2)
        navegador.get(link)
        sleep(2)
        # print(navegador)
        soup = BeautifulSoup(navegador.page_source, 'html.parser')
        titulo_reclamacao = soup.find('h1', attrs={'class': 'lzlu7c-3 berwWw'}).text
        localizacao = soup.find('span', attrs={'data-testid': 'complaint-location'}).text
        data_criacao = soup.find('span', attrs={'data-testid': 'complaint-creation-date'}).text
        id_reclamacao = soup.find('span', attrs={'data-testid': 'complaint-id'}).text
        status_reclamacao = soup.find('div', attrs={'data-testid': 'complaint-status'}).text
        try:
            compraria_novamente = soup.find('div', attrs={'data-testid': 'complaint-deal-again'}).text
            nota_atendimento = soup.find('div', attrs={'class': 'uh4o7z-3 ceUcTc'}).text
            consideracao_final_consumidor = soup.find('p', attrs={'class': 'sc-1o3atjt-4 JkSWX'}).text
        except:
            compraria_novamente = ''
            nota_atendimento = ''
            consideracao_final_consumidor = ''
            
        reclamacao = {
            'titulo': titulo_reclamacao,
            'localizacao': localizacao,
            'data_criacao': data_criacao,
            'id_reclamacao': id_reclamacao,
            'status': status_reclamacao,
            'compraria_novamente': compraria_novamente,
            'nota_atendimento': nota_atendimento,
            'consideracao_final_consumidor': consideracao_final_consumidor
        }

        lista_reclamacoes.append(reclamacao)

        
    return lista_reclamacoes

try: 
    ult_pag = ultima_pag()   
        
    for x in range(1,ult_pag+1):
        main(x)
        
    df = pd.DataFrame(lista_reclamacoes)
    df = df.drop(index=0)
    df.to_csv(f'.\data\data-{datetime.date.today()}.csv', index=False) 
except Exception as e:
    errorlist.append(f'{e} em {datetime.date.today()}')
    f = open('logs_error.txt', 'a')
    f.write(str(errorlist))
    f.close()
finally:
    print(f'Done. {datetime.date.today()}')
