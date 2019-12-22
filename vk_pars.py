import vk_api
import random
import sqlite3 #SQLite
import requests  # http 
from bs4 import BeautifulSoup   # суп html
import re   # регулярки
import copy



# PARSING
def isi_text(j):
    pattern = re.compile(r'\w+[А-Яа-яёЁA-Z0-9.,-:₽]+')
    i = ' '.join(pattern.findall(j))
    return i

def isi_text_2(j):
    pattern = re.compile(r'\w+')
    i = ' '.join(pattern.findall(j))
    return i

def isi_text_3(j):
    pattern = re.compile(r'[0-9]+₽')
    i = ' '.join(pattern.findall(j))
    return i

def remove_all(string):
    pattern = re.compile(r'[А-Яа-яёЁ0-9 ]+')
    return pattern.findall(string)[0].strip()




# KARO
def find_all_theaters_KARO(theatres):
    dicti = {}
    metro_class = 'cinemalist__cinema-item__metro__station-list__station-item'
    for theater in theatres:
        dicti[theater.findAll('h4')[0].text] = {
            'metro': [remove_all(i.text) for i in theater.findAll('li', class_=metro_class)] , 
            'address': theater.findAll('p')[0].text.split('+')[0].strip()  ,
            'phone': '+7 ' + isi_text(theater.findAll('p')[0].text.split('+')[-1])  ,
            'data_id': theater['data-id']
        }
    return dicti 

def name_theater():
    for j in name_knt:
        name_teat = j.findAll('h2')[0].text
    return name_teat

def film_time(film_s):
    spisok =[]
    dickti = {}
    dickti2 = {}
    for film in film_s:
        dickti2 = {}
        for i in film.findAll('div', class_ = 'cinema-page-item__schedule__row__board-row'):
            time_sp = []
            time_D = i.findAll('div', class_ = 'cinema-page-item__schedule__row__board-row__left')[0].text.strip()
            
            time = i.findAll('div', class_ = 'cinema-page-item__schedule__row__board-row__right')[0].findAll('a')
            time = [j.text for j in time]
            time_sp.append(time)
            dickti2[time_D] = time_sp
            dickti[film.findAll('h3')[0].text] = dickti2
    return (dickti)

id_karo = ['1','3','4','6','8','9','10','11','12','13','15','33','34','35','39','44']

url = "https://karofilm.ru"
url_theaters = url + "/theatres"

r_k = requests.get(url_theaters)
if r_k.status_code == 200:
    soup = BeautifulSoup(r_k.text, "html.parser")
    theaters = soup.findAll('li', class_='cinemalist__cinema-item')
    karo_theatres = find_all_theaters_KARO(theaters)
else:
    print("Страница не найдена")

karo_dict = {}
for id_ in id_karo:
    url = 'https://karofilm.ru/'
    url_karo_ft = url + "/theatres?id=" + id_
    r_karo_ft = requests.get(url_karo_ft)
    if r_karo_ft.status_code == 200:
        soup_f = BeautifulSoup(r_karo_ft.text, "html.parser")
        film_s = soup_f.findAll('div', class_='cinema-page-item__schedule__row')  

        name_knt = soup_f.findAll('div', class_='cinema-page-item__title__left')  
        karo_films = film_time(film_s)
        karo_dict.setdefault(id_, karo_films)
    else:
        print("Страница не найдена")

answer1 = karo_dict
answer = copy.deepcopy(answer1)
for a in answer1:
    for b in answer1[a]:
        if '2D' in answer1[a][b].keys():
            pass
        else:
            answer[a][b]['2D'] = ''

        if '3D' in answer1[a][b].keys():
            pass
        else:
            answer[a][b]['3D'] = ''
        if 'BLACK 2D' in answer1[a][b].keys():
            pass
        else:
            answer[a][b]['BLACK 2D'] = ''

        if 'КАРОакция' in answer1[a][b].keys():
            pass
        else:
            answer[a][b]['КАРОакция'] = ''

    #SQL  KARO

 
conn = sqlite3.connect("karo_.db") 
cursor = conn.cursor()
cursor.execute('drop table karo_')


cursor.execute("""CREATE TABLE IF NOT EXISTS karo_(
                id integer PRIMARY KEY,
                brand_id integer,
                name text,
                address text,
                metro text,
                phone text,
                name_film text,
                time_2D text,
                time_3D text,
                BLACK_2D text,
                KAROakci text
                )""")
conn = sqlite3.connect("karo_.db") 
cursor = conn.cursor()

for key, item in karo_theatres.items():
    dta_id = item['data_id']
    adre = item['address']
    metro = ', '.join(item['metro'])
    phone = item['phone']
    adre = re.sub('"', '', adre)
    for i in answer[dta_id]:
        name_film = i
        time_2D = answer[dta_id][i]['2D']
        time_3D = answer[dta_id][i]['3D']
        BLACK_2D = answer[dta_id][i]['BLACK 2D']
        KAROakci = answer[dta_id][i]['КАРОакция']
        cursor.execute(f'insert into karo_ (brand_id, name, address, metro, phone, name_film, time_2D, time_3D, BLACK_2D, KAROakci) values ("{dta_id}","{key}","{adre}","{metro}","{phone}","{name_film}","{time_2D}","{time_3D}","{BLACK_2D}","{KAROakci}")')
conn.commit()







# CINEMA
def find_all_theaters_cinema(theaters2, id_cinema):
    dicti = {}
    i = -1
    metro_class = 'cinemalist__cinema-item__metro__station-list__station-item'
    for theater in theaters2:
        i += 1
        dicti[id_cinema[i]] = {
            'name': isi_text(theater.findAll('h3')[0].text),
            'metro': isi_text(theater.findAll('span', class_='sub_title')[1].text).replace(' ',', '),
            'address': theater.findAll('span')[0].text.split('+')[0].strip(),
        }
    return dicti 

def find_time(films_cinema):
    all_f = {}
    p = []
    for film in films_cinema:
        for i in film.findAll('div', class_='shedule_movie bordered gtm_movie'):
            name = isi_text(i.findAll('span')[1].text)
            k = len(i.findAll('a')) 
            p = []
            for x in range(k-1):
                time = isi_text(i.findAll('a')[x+1].text)
                p.append(time)
                all_f[name] = p
    return(all_f)

id_cinema = ['/belaya-dacha/', '/butovo-mall/', '/waypark/', '/global-city/', '/gorizont/', '/evropa/', '/zelenopark/', '/kaluzhskij/', '/kutuzovskiy/', '/ladoga/', '/lefortovo/', '/metropolis/', '/michurinsky/', '/mozhayka/', '/oblaka/', '/polezhaevskiy/', '/5avenu/', '/rivera/', '/semenovsky/', '/city/', '/tepliy-stan/', '/filion/', '/mega-himki/', '/cdm/', '/chertanovo/']

cinema_dict ={}
for id_ in id_cinema:
    url_cinema = 'https://kinoteatr.ru'
    url_cinema_t = url_cinema + '/raspisanie-kinoteatrov/'
    url_cinema_f = url_cinema_t + id_

    r_cinema_t = requests.get(url_cinema_t)
    r_cinema_f = requests.get(url_cinema_f)
    if r_cinema_t.status_code == 200:
        soup2 = BeautifulSoup(r_cinema_t.text, "html.parser")
        soup2_2 = BeautifulSoup(r_cinema_f.text, "html.parser")

        films_cinema = soup2_2.findAll('div', class_='shedule_content gtm-ec-list')

        theaters2 = soup2.findAll('div', class_='col-md-12 cinema_card')
        
        dicti_cinema_theaters = {}
        cinema_theatres = find_all_theaters_cinema(theaters2, id_cinema)
        
        cinema_films = find_time(films_cinema)
        cinema_dict[id_] = cinema_films
    else:
        print("Страница не найдена")


    #SQL  CINEMA PARK 

conn_2 = sqlite3.connect("cinema__.db")
cursor_2 = conn_2.cursor()
cursor_2.execute('drop table cinema__')

cursor_2.execute("""CREATE TABLE IF NOT EXISTS cinema__(
                id integer PRIMARY KEY,
                brand_id integer,
                name text,
                address text,
                metro text,
                name_film text,
                info text
                )""")

conn_2 = sqlite3.connect("cinema__.db")
cursor_2 = conn_2.cursor()

#SQL  CINEMA PARK 
for key, item in cinema_theatres.items():
    name = item['name']
    metro_cinema = item['metro']
    address_cinema = item['address']
    id_c = key
    for i in cinema_dict[id_c].items():
        name_film_cinema = i[0]
        info = i[1]
        
        cursor_2.execute(f'insert into cinema__ (brand_id, name, address, metro, name_film, info) values ("{id_c}","{name}","{address_cinema}","{metro_cinema}","{name_film_cinema}","{info}")')
conn_2.commit()






#KINO MAX
def find_all_theaters_KINOMAX(theatres):
    dicti = {}

    for theater in theatres:
        data_id_list_max.append(theater.findAll('a')[0].get('href'))
        dicti[theater.findAll('a')[0].text] = {
            'metro': theater.findAll('div', class_='fs-08')[0].text.split('·')[0].strip(), 
            'address': theater.findAll('div', class_='fs-08')[-1].text.split('·')[-1].strip(),
            'data-id': theater.findAll('a')[0].get('href')
        }
    return dicti

def film_time_max(film_max,id_):
    all_films = {}
    info = {}
    time_spisok = []
    for film in film_max:
        info ={}
        for i in range(len(film.findAll('div', class_='d-flex w-100 schedule-row'))):
            time_d = film.findAll('div', class_ = 'w-10 format-tag')[i].text[12:-10] 
            time = [j.text for j in film.findAll('div', class_='d-flex w-100 schedule-row')[i].findAll('a')] 
            cost = [j.text[17:-15] for j in film.findAll('div', class_='d-flex w-100 schedule-row')[i].findAll('div', class_='fs-07 text-main pt-2 text-center')]
            info[time_d] = []

            if len(cost) != len(time):
                time = time[1:]

            for j in range(len(cost)):
                info[time_d].append(dict(time=time[j], price=cost[j]))

        all_films[film.findAll('div', class_ = 'w-70')[0].text[1:-1]] = info
    return all_films



url_theaters = "https://kinomax.ru/finder"
r = requests.get(url_theaters)
if r.status_code == 200:
    soup_max = BeautifulSoup(r.text, "html.parser")
    theaters = soup_max.findAll('div', class_='pt-3 pb-3')
    
    data_id_list_max = []
    kinomax_theatres = find_all_theaters_KINOMAX(theaters)####### кинотеатры

    for i in kinomax_theatres.items():
        data_id_list_max.append(i[1]['data-id'])
else:
    print("Страница не найдена")




kinomax_dicti = {}
for id_ in data_id_list_max:
    url_max = "https://kinomax.ru"
    url_theaters = url_max + "/finder"
    url_films = url_max + id_  
    
    r = requests.get(url_films)
    if r.status_code == 200:
        s_max = BeautifulSoup(r.text, "html.parser")
        film_max = s_max.findAll('div', class_='d-flex border-bottom-1 border-stack film')    
        kinomax_films = film_time_max(film_max, id_)######### фильмы
        
        kinomax_dicti[id_]= kinomax_films
        
    else:
        print("Страница не найдена")


#  SQL  KINO MAX

conn_3 = sqlite3.connect("kino_max.db")
cursor_3 = conn_3.cursor()
cursor_3.execute('drop table kino_max')


cursor_3.execute("""CREATE TABLE IF NOT EXISTS kino_max(
                id integer PRIMARY KEY,
                brand_id integer,
                name text,
                address text,
                metro text,
                name_film text,
                info text
                )""")

conn_3 = sqlite3.connect("kino_max.db")
cursor_3 = conn_3.cursor()

for key, item in kinomax_theatres.items():
    
    metro = item['metro']
    adre = item['address']
    brand_id = item['data-id']
    name = key
    for i in kinomax_dicti[brand_id].items():
        name_film = i[0]
        info = i[1]
        cursor_3.execute(f'insert into kino_max (brand_id, name, address, metro, name_film, info) values ("{brand_id}","{name}","{adre}","{metro}","{name_film}","{info}")')
conn_3.commit()

