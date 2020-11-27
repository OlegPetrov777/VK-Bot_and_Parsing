import vk_api
import random
import sqlite3 #SQLite
import requests  # http 
from bs4 import BeautifulSoup   # суп html
import re   # регулярки
import time

conn = sqlite3.connect("karo_.db") 
cursor = conn.cursor()


conn_2 = sqlite3.connect("cinema__.db") 
cursor_2 = conn_2.cursor()


conn_3 = sqlite3.connect("kino_max.db")
cursor_3 = conn_3.cursor()


def isi_text(j):
    pattern = re.compile(r'\w+[А-Яа-яёЁA-Z0-9.,-:₽]+')
    i = ' '.join(pattern.findall(j))
    return i

# 0 = 9
token = "c5e63605b88c44ae6dae4c0717b42a8bb7e19f4fff1a8f3cc5b2275ece089c44cfb41b74efbb894075e80"

vk = vk_api.VkApi(token=token)
vk._auth_token()

while True:
    
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]

            #privet
            if body.lower() == "привет" or body.lower() == "Привет": 
                vk.method("messages.send", {"peer_id": id, "message": "Привет)", "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send", {"peer_id": id,
                    "message": "Чтобы начать напишите: \"/start\" ",
                    "random_id": random.randint(1, 2147483647)})

            
            elif body.lower() == "/start":
                vk.method("messages.send", {"peer_id": id,
                    "message": "Какая киносеть тебе нужна? \n1. КАРО\n/karo_cinemas\n2. Синема Парк\n/cinema_cinemas\n3. Киномакс\n/kinomax_cinemas",
                    "random_id": random.randint(1, 2147483647)})
# KARO
            elif body.lower() == '/karo_cinemas':
                
                karo_t_list = list(cursor.execute("select distinct name from karo_"))
                karo_t_list_2 = []
                
                for i in karo_t_list:
                    karo_t_list_2.append(i[0])
                mess = []
                for i, e in enumerate(karo_t_list_2, 1):
                    mess.append(f'{i}. {e}')
                m = ''
                for j in mess:
                    m = m + j + '\n'
                vk.method("messages.send", {"peer_id": id, "message": m, "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send", {"peer_id": id,
                    "message": "Чтобы выбрать кинотеатр напишите \"/karo_cinemas_\" и в конце его номер.",
                    "random_id": random.randint(1, 2147483647)})
        #Theatres info karo
            elif body.lower()[:14] == '/karo_cinemas_': 
                num = int(body.lower()[14:]) - 1
                if num>=0 and num<16:

                    karo_t_list = list(cursor.execute("select distinct name from karo_"))
                    karo_t_list_2 = []
                    karo_info_a = list(cursor.execute("select distinct address from karo_"))
                    karo_a = []
                    karo_info_m = list(cursor.execute("select distinct metro from karo_"))
                    karo_m = []
                    karo_info_p = list(cursor.execute("select distinct phone from karo_"))
                    karo_p = []

                    for i in karo_t_list:
                        karo_t_list_2.append(i[0])
                    for i in karo_info_a:
                        karo_a.append(i[0])
                    for i in karo_info_m:
                        karo_m.append(i[0])
                    for i in karo_info_p:
                        karo_p.append(i[0])

                    mm = karo_t_list_2[num]+'\n'+ 'адрес: ' + karo_a[num]+'\n' + 'метро: ' + karo_m[num]+'\n' + 'номер телефона: ' + karo_p[num]
                    vk.method("messages.send", {"peer_id": id, "message":f'{num+1}. {mm} ', "random_id": random.randint(1, 2147483647)})
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Чтобы посмотреть список фильмов в кинотеатре, напишите \"/karo_films_\" и его номер." ,
                        "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {"peer_id": id, "message": "Нет такого кинотеатра!", "random_id": random.randint(1, 2147483647)})

            #FILMS karo
            elif body.lower()[:12] == '/karo_films_':
                num = int(body.lower()[12:]) - 1
                if num>=0 and num<16:

                    karo_t_id = list(cursor.execute("select distinct brand_id from karo_"))
                    karo_t_id_2 = []
                    for i in karo_t_id:
                        karo_t_id_2.append(i[0]) 
                    karo_t_id_2 = karo_t_id_2[num] 

                    karo_fi = list(cursor.execute(f"select distinct name_film from karo_ where brand_id = '{karo_t_id_2}'"))
                    karo_fii = []

                    for i in karo_t_list:
                        karo_t_list_2.append(i[0])
                    for i in karo_fi:
                        karo_fii.append(i[0])   

                    mess = []
                    for i, e in enumerate(karo_fii, 1):
                        mess.append(f'{i}. {e}')
                    n = ''
                    for j in mess:
                        n = n + j + '\n'

                    nn = karo_t_list_2[num]+': \n'+ n

                    vk.method("messages.send", {"peer_id": id, "message": f'{nn}' , "random_id": random.randint(1, 2147483647)})
                    vk.method("messages.send",
                        {"peer_id": id, "message":
                        'Чтобы посмотреть список сеансов для фильма, напишите \n/karo_time_\"номер кинотеатра\" _ \"номер фильма\" ',
                        "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {"peer_id": id, "message": "Нет такого кинотеатра!", "random_id": random.randint(1, 2147483647)})

            # TIME karo
            elif body.lower()[:11] == '/karo_time_':
                num_num = body.lower()[11:].split('_')
                num_t = int(num_num[0]) -1
                num_f = int(num_num[1]) -1 
                if num_t>=0 and num_t<16:

                    karo_t_id = list(cursor.execute("select distinct brand_id from karo_"))
                    karo_t_id_2 = []
                    for i in karo_t_id:
                        karo_t_id_2.append(i[0]) 
                    karo_t_id_2 = karo_t_id_2[num_t] 

                    karo_fi = list(cursor.execute(f"select distinct name_film from karo_ where brand_id = '{karo_t_id_2}'"))
                    karo_fii = []
                    for i in karo_fi:
                        karo_fii.append(i[0]) 
                    

                    if num_f>=0 and num_f<len(karo_fii):


                    
                        karo_fii2 = karo_fii[num_f]


                        karo_2D = list(cursor.execute(f"select distinct time_2D from karo_ where name_film = '{karo_fii2}'"))
                        if karo_2D[0][0] == '':
                            k_2D = '4444'
                        else:
                            k_2D = []
                            for i in karo_2D:
                                k_2D.append(i[0])
           
                        karo_3D = list(cursor.execute(f"select distinct time_3D from karo_ where name_film = '{karo_fii2}'"))
                        if karo_3D[0][0] == '':
                            k_3D = '4444'
                        else:
                            k_3D = []
                            for i in karo_3D:
                                k_3D.append(i[0])

                        karo_black = list(cursor.execute(f"select distinct BLACK_2D from karo_ where name_film = '{karo_fii2}'"))
                        if karo_black[0][0] == '':
                            k_black = '4444' 
                        else:
                            k_black = []
                            for i in karo_black:
                                k_black.append(i[0])

                        karo_akci = list(cursor.execute(f"select distinct KAROakci from karo_ where name_film = '{karo_fii2}'"))
                        if karo_akci[0][0] =='':
                            k_akci = '4444'
                        else:
                            k_akci = []
                            for i in karo_akci:
                                k_akci.append(i[0])

                        k_all_time = karo_fii2 + ':'
                        if k_2D[0][2:-2] != '':
                            k_all_time = k_all_time + '\n' + '2D:  ' + k_2D[0][2:-2]
                        if k_3D[0][2:-2] != '':
                            k_all_time = k_all_time + '\n' + '3D:  ' + k_3D[0][2:-2]
                        if k_black[0][2:-2] != '':
                            k_all_time = k_all_time + '\n' + 'BLACK_2D:  ' + k_black[0][2:-2]
                        if k_akci[0][2:-2] != '':
                            k_all_time = k_all_time + '\n' + 'KAROakci:  ' + k_akci[0][2:-2]


                  
                        vk.method("messages.send",
                            {"peer_id": id,
                            "message": f"{k_all_time}",
                            "random_id": random.randint(1, 2147483647)})    

                    else:
                        vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Такого фильма нет!",
                        "random_id": random.randint(1, 2147483647)})

                else:
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Такого кинотеатра нет!",
                        "random_id": random.randint(1, 2147483647)})












# CINEMA
            elif body.lower() == '/cinema_cinemas':
                cinema_t_list = list(cursor_2.execute("select distinct name from cinema__"))
                cinema_t_list_2 = []
                
                for i in cinema_t_list:
                    cinema_t_list_2.append(i[0])
                mess_c = []
                for i, e in enumerate(cinema_t_list_2, 1):
                    mess_c.append(f'{i}. {e}')
                m_c = ''
                for j in mess_c:
                    m_c = m_c + j + '\n'
                vk.method("messages.send", {"peer_id": id, "message": m_c, "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send",
                    {"peer_id": id,
                    "message": "Чтобы выбрать кинотеатр напишите \"/cinema_cinemas_\" и в конце его номер.",
                    "random_id": random.randint(1, 2147483647)})

            
       # INFO cinema     
            elif body.lower()[:16] == '/cinema_cinemas_':
                num_c = int(body.lower()[16:])-1
                if num_c>=0 and num_c<25:
                    cinema_t_list = list(cursor_2.execute("select distinct name from cinema__"))
                    cinema_t_list_2 = []
                    cin_info_a = list(cursor_2.execute("select distinct address from cinema__"))
                    cin_a = []
                    cin_info_m = list(cursor_2.execute("select distinct metro from cinema__"))
                    cin_m = []

                    for i in cinema_t_list:
                        cinema_t_list_2.append(i[0])
                    for i in cin_info_a:
                        cin_a.append(i[0])
                    for i in cin_info_m:
                        cin_m.append(i[0])

                    cc = cinema_t_list_2[num_c]+':\n'+ 'адрес: ' + cin_a[num_c]+'\n' + 'метро: ' + cin_m[num_c]+'\n'
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message":f'{num_c+1}. {cc} ',
                        "random_id": random.randint(1, 2147483647)})
                    
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Чтобы посмотреть список фильмов в кинотеатре, напишите \"/cinema_films_\" и номер кинотеатра." ,
                        "random_id": random.randint(1, 2147483647)})

                else:
                    vk.method("messages.send", {"peer_id": id, "message": 'Такого кинотеатра нет!', "random_id": random.randint(1, 2147483647)})
        # FILMS cinema

            elif body.lower()[:14] == '/cinema_films_': 
                num_c = int(body.lower()[14:]) - 1
                if num_c>=0 and num_c<25:

                    cin_id = list(cursor_2.execute("select distinct brand_id from cinema__"))
                    cin_id_2 = []
                    for i in cin_id:
                        cin_id_2.append(i[0]) 
                    cin_id_2 = cin_id_2[num_c] 

                    cin_fi = list(cursor_2.execute(f"select distinct name_film from cinema__ where brand_id = '{cin_id_2}'"))
                    cin_fii = []

                    for i in cinema_t_list:
                        cinema_t_list_2.append(i[0])
                    for i in cin_fi:
                        cin_fii.append(i[0])   

                    mess = []
                    for i, e in enumerate(cin_fii, 1):
                        mess.append(f'{i}. {e}')
                    n = ''
                    for j in mess:
                        n = n + j + '\n'

                    nn = cinema_t_list_2[num_c]+': \n'+ n

                    vk.method("messages.send", {"peer_id": id, "message": f'{nn}' , "random_id": random.randint(1, 2147483647)})
                    
                    vk.method("messages.send",
                        {"peer_id": id, "message":
                        'Чтобы посмотреть список сеансов для фильма, напишите \n/cinema_time_ \"номер кинотеатра\" _ \"номер фильма\" ',
                        "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {"peer_id": id, "message": "Нет такого кинотеатра!", "random_id": random.randint(1, 2147483647)})
    # TIME cinema
            elif body.lower()[:13] == '/cinema_time_':
                num_num_c = body.lower()[13:].split('_')
                num_c_t = int(num_num_c[0]) - 1
                num_c_f = int(num_num_c[1]) - 1

                if num_c_t>=0 and num_c_t<25 and num_c_f>=0:

                    cin_id = list(cursor_2.execute("select distinct brand_id from cinema__"))
                    cin_id_2 = []
                    for i in cin_id:
                        cin_id_2.append(i[0]) 
                    cin_id_2 = cin_id_2[num_c_t] 

                    cin_fi = list(cursor_2.execute(f"select distinct name_film from cinema__ where brand_id = '{cin_id_2}'"))
                    cin_fii = []
                    for i in cin_fi:
                        cin_fii.append(i[0]) 

                    if num_c_f>=0 and num_c_f<len(cin_fii):


                        cin_fii2 = cin_fii[num_c_f]

                        cin_info = list(cursor_2.execute(f"select distinct info from cinema__ where name_film = '{cin_fii2}' and brand_id = '{cin_id_2}'"))
                        cc = str(cin_info)[4:-5]

                        c_all_time = cin_fii2 + ':\n'+  cc
                        vk.method("messages.send",
                            {"peer_id": id,
                            "message": f"{c_all_time}",
                            "random_id": random.randint(1, 2147483647)})


                    else:
                        vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Такого фильма нет!",
                        "random_id": random.randint(1, 2147483647)})

                else:
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Такого кинотеатра нет!",
                        "random_id": random.randint(1, 2147483647)})







# KINO MAX  
            elif body.lower() == '/kinomax_cinemas':
                max_t_list = list(cursor_3.execute("select distinct name from kino_max"))
                max_t_list_2 = []
                
                for i in max_t_list:
                    max_t_list_2.append(i[0])
                mess_max = []
                for i, e in enumerate(max_t_list_2, 1):
                    mess_max.append(f'{i}. {e}')
                m_m = ''
                for j in mess_max:
                    m_m = m_m + j + '\n'
                vk.method("messages.send", {"peer_id": id, "message": m_m, "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send",
                    {"peer_id": id,
                    "message": "Чтобы выбрать кинотеатр напишите \"/kinomax_cinemas_\" и в конце его номер.",
                    "random_id": random.randint(1, 2147483647)})

#MAX  cinemas
            elif body.lower()[:17] == '/kinomax_cinemas_':
                num_m = int(body.lower()[17:])-1
                if num_m>=0 and num_m<9:
                    max_t_list = list(cursor_3.execute("select distinct name from kino_max"))
                    max_t_list_2 = []
                    max_info_a = list(cursor_3.execute("select distinct address from kino_max"))
                    max_a = []
                    max_info_m = list(cursor_3.execute("select distinct metro from kino_max"))
                    max_m = []

                    for i in max_t_list:
                        max_t_list_2.append(i[0])
                    for i in max_info_a:
                        max_a.append(i[0])
                    for i in max_info_m:
                        max_m.append(i[0])

                    maxx = max_t_list_2[num_m]+':\n'+ 'адрес: ' + max_a[num_m]+'\n' + 'метро: ' + max_m[num_m]+'\n'
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message":f'{num_m+1}. {maxx} ',
                        "random_id": random.randint(1, 2147483647)})
                    
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Чтобы посмотреть список фильмов в кинотеатре, напишите \"/kinomax_films_\" и номер кинотеатра." ,
                        "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {"peer_id": id, "message": 'Такого кинотеатра нет!', "random_id": random.randint(1, 2147483647)})

    # MAX films

            elif body.lower()[:15] == '/kinomax_films_': 
                num_m = int(body.lower()[15:]) - 1
                if num_m>=0 and num_m<9:

                    max_id = list(cursor_3.execute("select distinct brand_id from kino_max"))
                    max_id_2 = []
                    for i in max_id:
                        max_id_2.append(i[0]) 
                    max_id_2 = max_id_2[num_m] 

                    max_fi = list(cursor_3.execute(f"select distinct name_film from kino_max where brand_id = '{max_id_2}'"))
                    max_fii = []

                    for i in max_t_list:
                        max_t_list_2.append(i[0])
                    for i in max_fi:
                        max_fii.append(i[0])   

                    mess = []
                    for i, e in enumerate(max_fii, 1):
                        mess.append(f'{i}. {e}')
                    n = ''
                    for j in mess:
                        n = n + j + '\n'

                    maxi = max_t_list_2[num_m]+': \n'+ n

                    vk.method("messages.send", {"peer_id": id, "message": f'{maxi}' , "random_id": random.randint(1, 2147483647)})
                    
                    vk.method("messages.send",
                        {"peer_id": id, "message":
                        'Чтобы посмотреть список сеансов для фильма, напишите \n/kinomax_time_\"номер кинотеатра\" _ \"номер фильма\" ',
                        "random_id": random.randint(1, 2147483647)})
                else:
                    vk.method("messages.send", {"peer_id": id, "message": "Нет такого кинотеатра!", "random_id": random.randint(1, 2147483647)})


            elif body.lower()[:14] == '/kinomax_time_':
                num_num_c = body.lower()[14:].split('_')
                num_m_t = int(num_num_c[0]) - 1
                num_m_f = int(num_num_c[1]) - 1

                if num_m_t>=0 and num_m_t<9:

                    max_id = list(cursor_3.execute("select distinct brand_id from kino_max"))
                    max_id_2 = []
                    for i in max_id:
                        max_id_2.append(i[0]) 
                    max_id_2 = max_id_2[num_m_t] 

                    max_fi = list(cursor_3.execute(f"select distinct name_film from kino_max where brand_id = '{max_id_2}'"))
                    max_fii = []
                    for i in max_fi:
                        max_fii.append(i[0]) 

                    if num_m_f>=0 and num_m_f<len(max_fii):


                        max_fii2 = max_fii[num_m_f]

                        max_info = list(cursor_3.execute(f"select distinct info from kino_max where name_film = '{max_fii2}' and brand_id = '{max_id_2}'"))
                        ccmm = isi_text(str(max_info))

                        for i, e in enumerate(ccmm):
                            if e =='₽':
                                ccmm = ccmm[:i-1] + '\n' + ccmm[i+1:]
                            


                        max_all_time = max_fii2 + ':\n'+  ccmm
                        vk.method("messages.send",
                            {"peer_id": id,
                            "message": f"{max_all_time}",
                            "random_id": random.randint(1, 2147483647)})


                    else:
                        vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Такого фильма нет!",
                        "random_id": random.randint(1, 2147483647)})

                else:
                    vk.method("messages.send",
                        {"peer_id": id,
                        "message": "Такого кинотеатра нет!",
                        "random_id": random.randint(1, 2147483647)})


            else:
                vk.method("messages.send", {"peer_id": id,
                    "message": "я не знаю, что такое:  \"" + str(body.lower()) + "\". Напишите /start",
                    "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        time.sleep(1)        #если программа не подключилась к серверм сразу, то она не заканчиается, а подключается заново

