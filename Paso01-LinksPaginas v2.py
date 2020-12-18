# Librerias
# ----------------------------------------------------------------------------------------------------
import time
import sys
import random
import requests # install requests
from bs4 import BeautifulSoup as bs # pip install beautifulsoup4
from datetime import datetime

# Functions
# ----------------------------------------------------------------------------------------------------
# Obtener el html de una clase / Get html from class
# ----------------------------------------------------------------------------------------------------
def get_htmlclass(classtype, classname):
    try:
        txtvalue = section.find(classtype, class_=classname)
        return txtvalue.text
    except:
        return ''

# Inicializacion
# ----------------------------------------------------------------------------------------------------
original_stdout = sys.stdout # Save a reference to the original standard output
now = datetime.now()
step01 = '01-Links_'
step02 = '02-Comercios_'
step03 = '03-Menu'
filename = 'JustEat_' + now.strftime("%y-%m-%d_%H-%M-%S") + '_.ASC'

# WebSite Scraping 
# ----------------------------------------------------------------------------------------------------
link = 'https://www.just-eat.es/a-domicilio/madrid'

# Estipular una navegador para realizar la solicitud
# ----------------------------------------------------------------------------------------------------
UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1", 
       "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
       )

#headers = {'User-Agent': 'Mozilla/5.0'}

# Class to Scraping
# ----------------------------------------------------------------------------------------------------
html_class = 'ul'
name_class = 'group-links'

html_tbl_class = 'section'
name_tbl_class = 'c-listing-item c-listing-item--withHeader c-card c-card--rounded--large'

# Load the webpage content
# ----------------------------------------------------------------------------------------------------
ua = UAS[random.randrange(len(UAS))]
headers = {'user-agent': ua}
r = requests.get(link, headers=headers, timeout=(3.05, 27))

# Comprobamos que la petición nos devuelve un Status Code = 200
# ----------------------------------------------------------------------------------------------------
status_code = r.status_code
if status_code == 200:

    # Convert to a beautiful soup object
    soup = bs(r.content, 'html.parser')
    
# links = soup.find_all('a', href=True)
# ----------------------------------------------------------------------------------------------------
    links = []
    ul = soup.find(html_class, class_=name_class) # group-links
    if ul:
        for li in ul.find_all('li'):
            a = li.find('a', href=True)
            if a:
                links.append(a['href'])
# ----------------------------------------------------------------------------------------------------
    with open(step01 + filename, 'w', encoding='utf8') as f:
        for link in links:
            f.write(link + '\n')

        f.close()
# ----------------------------------------------------------------------------------------------------
with open(step01 + filename, 'r', encoding='utf8') as f:
    cnt = 1
    link = f.readline()
    while link:
        # Load the webpage content
        ua = UAS[random.randrange(len(UAS))]
        headers = {'user-agent': ua}
        r = requests.get(link.replace('\n', ''), headers=headers, timeout=(3.05, 27))
        # Comprobamos que la petición nos devuelve un Status Code = 200
        status_code = r.status_code            
        if status_code == 200:
# ----------------------------------------------------------------------------------------------------
            # Convert to a beautiful soup object
            soup = bs(r.content, 'html.parser')            

            # Determinar la parte del HTML de donde se recolectaran los datos
            sectionList = soup.findAll(html_tbl_class, class_=name_tbl_class)

            if sectionList:
                with open(step02 + filename, 'a+', encoding='utf8') as sf:
                    for section in sectionList:
                        Elem_Id = section.get('data-restaurant-id') # IdRestaurante
                        Ref_Menu = section.find('a', class_='c-listing-item-link u-clearfix') # Menu Link
                        Elem_Link = Ref_Menu.get('href') 

                        Col01 = get_htmlclass('h3', 'c-listing-item-title') # Nombre Empresa
                        Col02 = get_htmlclass('span', 'is-visuallyHidden') # Ranking 
                        Col03 = get_htmlclass('strong', 'c-listing-item-ratingText') # Numero de Valoraciones
                        Col04 = get_htmlclass('p', 'c-listing-item-text c-listing-item-detailsRow-text c-listing-item-promo-text') # Descuento a Partir 
                        Col05 = get_htmlclass('p', 'c-listing-item-text c-listing-item-detailsRow-text u-color-secondary') # Picante, Vegetariano
                        Col06 = get_htmlclass('p', 'c-listing-item-text c-listing-item-detailsRow-text c-badge c-listing-item-badge c-badge--transparent c-badge--noPad')  # Costo Entrega - Pago Minimo
                        Col07 = get_htmlclass('p', 'c-listing-item-text c-listing-item-detailsRow-text')    # Tiempo de Entrega
                        Col08 = get_htmlclass('span', 'c-listing-item-label c-badge c-badge--angled')   # Patrocinado
                        Col09 = get_htmlclass('p', 'c-listing-item-text c-badge c-listing-item-badge c-badge--transparent c-badge--noPad') # Tipo de Cocina
                                    
                        TxtRow = link + '|' + Elem_Id + '|' +  Elem_Link + '|' + now.strftime("%Y-%m-%d") + '|' + Col01 + '|' +  Col02 + '|' +  Col03 + '|' +  Col04 + '|' +  Col05 + '|' +  Col06 + '|' +  Col07 + '|' +  Col08 + '|' +  Col09
                        TxtRow = TxtRow.replace('\n', '-').replace('\r', ';') #+ ' \n'

                        sf.write(TxtRow + ' \n')                    
                
                sf.close()
            else:
                print('Error: No se cargo bien la pagina')                
# ----------------------------------------------------------------------------------------------------
        time.sleep(10)        
# ----------------------------------------------------------------------------------------------------        
        cnt += 1
        link = f.readline()
