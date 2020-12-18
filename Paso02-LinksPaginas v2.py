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
        txtvalue = dom.find(classtype, class_=classname)
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
rootweb = 'https://www.just-eat.es'

# Estipular una navegador para realizar la solicitud
# ----------------------------------------------------------------------------------------------------
UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1", 
       "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
       "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
       )

# headers = {'User-Agent': 'Mozilla/5.0'}

link = 'https://www.just-eat.es/restaurants-homeburgerbarmadrid/menu'
link = 'https://www.just-eat.es/restaurants-foodexpress/menu'

# ----------------------------------------------------------------------------------------------------
html_class = 'div'
name_class = 'tabs '

html_tbl_class = 'section'
name_tbl_class = 'menuCard-category accordion accordion--ruled is-open'

html_menu_class = 'div'
name_menu_class = 'menu-product product u-separated--dash'

# ----------------------------------------------------------------------------------------------------
with open('02-Comercios_JustEat_20-08-14_11-30-31_.ASC', 'r', encoding='utf8') as f:
    cnt = 1
    link = f.readline()

    while link:
        record = link.split("|")    
        link = rootweb + record[2] + '/'
        Id_Comercio = record[1]

        # wait n
        # 
        # ext read
        time.sleep(10)
#  Load the webpage content
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
            div = soup.find(html_class, class_=name_class)  
            if div:
                for a in div.find_all('a'):
                    links.append(a['href'])

            if not links:
                print('Error: No encontro class:' + name_class + ' Linea:'+str(cnt) + ' Comercio:' + Id_Comercio)

#            for link in links:
# Recolectar datos del Menu        
# ----------------------------------------------------------------------------------------------------        
            if link.find('menu') > 0 or 1==1:
                sections = soup.findAll(html_tbl_class, class_=name_tbl_class)  

                if sections:
                    with open(step03 + filename, 'a+', encoding='utf8') as sf:
                        for section in sections: 
                            dom = section
                            Col01 = get_htmlclass('h3', 'menuCard-category-title gamma accordion-header icon')

                            items = section.findAll(html_menu_class, class_=name_menu_class)  
                            if items:
                                for item in items:
                                    dom = item
                                    Prod_Id = item.get('data-product-id')

                                    Col02 = get_htmlclass('h4', 'product-title')
                                    Col03 = get_htmlclass('div', 'product-description')
                                    Col04 = get_htmlclass('div', 'product-price u-noWrap')
                                    
                                    Prod_Att_02 = ''
                                    Prod_Att_03 = ''

                                    dom = item.find('button', 'btn btn--primary btn--roundedIcon btn-addproduct')
                                    if dom:
                                        Prod_Att_01 = 'true'
                                    else:
                                        Prod_Att_01 = 'false'
                                    dom = item.find('i', 'icon icon-product icon-product--spicy')
                                    if dom:
                                        Prod_Att_02 = dom.get('title')
                                    dom = item.find('i', 'icon icon-product icon-product--vegetarian')
                                    if dom:
                                        Prod_Att_03 = dom.get('title')

                                    TxtRow = Id_Comercio + '|' + Prod_Id + '|' + Prod_Att_01 + '|' +  Prod_Att_02 + '|' +  Prod_Att_03 + '|' + now.strftime("%Y-%m-%d") + '|' + Col01 + '|' +  Col02 + '|' +  Col03 + '|' +  Col04 
                                    TxtRow = TxtRow.replace('\n', '-').replace('\r', ';') #+ ' \n'

                                    sf.write(TxtRow + ' \n')

                        sf.close()    
                else:
                    print('Error: No existen seccions Linea:' + str(cnt) + ' Comercio:' + Id_Comercio)   
            else:
                    print('Warning: Sin menu Linea:' + str(cnt) + ' Comercio:' + Id_Comercio)   
        cnt += 1
        link = f.readline()    

    else:
        print('Error: No encontro pagina HTML Linea:'+ str(cnt) + ' Comercio:' + Id_Comercio) 

f.close()                      
