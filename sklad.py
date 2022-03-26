#!/usr/bin/python
import psycopg2
from config import config
import tkinter
from tkinter import *
from tkinter import messagebox
def connect(article):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        cur.execute('select * from public.inventory where article = %s'%article)

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
       
    # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return db_version

def str_to_num(line):
        """функция конвертирует строку в число"""
        line = line.strip()
        # если в строке только цифры
        if line.isdigit():
            return int(line) 
        # если строка содержит точку или запятую
        elif '.' in line or ',' in line:
            # если из строки убрать точку или запятую
            # и при этом в строке останутся только цифры
            if any(line.replace(x, '').isdigit() for x in ['.', ',']):
                return float(line.replace(',', '.'))
        else:
            # ошибка
            print('Это не число!\n')
            return None

def new_button():

    btn_search.config(command=lambda:[lbl_article_found.pack_forget(), lbl_name.pack_forget(), lbl_quantity.pack_forget(), lbl_location.pack_forget(), clicked_search()])

def new_button_admin():

    btn_search.config(command=lambda:[lbl_article_found.pack_forget(), lbl_name.pack_forget(), lbl_quantity.pack_forget(), lbl_location.pack_forget(), lbl_supplier.pack_forget(), lbl_date_last_supply.pack_forget(), lbl_date_next_supply.pack_forget(), lbl_time_turnover.pack_forget(), clicked_search_admin()])

        
def clicked():
    res_log = txt_log.get()
    res_pass = txt_pass.get()
    global window_auth
    global window_search
    global txt_article
    global btn_search
    if res_log == "admin" and res_pass == "1":
        window_auth.destroy()
        window_search = Tk()  
        window_search.title("Поиск")  
        window_search.geometry('500x300')  
        lbl_article = Label(window_search, text="Артикул")  
        lbl_article.pack(pady=10)
        txt_article = Entry(window_search,width=10)  
        txt_article.pack()
        btn_search = Button(window_search, text="Поиск", command=lambda:[new_button_admin(), clicked_search_admin()])  
        btn_search.pack(pady=5)

        window_search.mainloop()
    if res_log == "user" and res_pass == "2":
        window_auth.destroy()
        window_search = Tk()  
        window_search.title("Поиск")  
        window_search.geometry('500x300')  
        lbl_article = Label(window_search, text="Артикул")  
        lbl_article.pack(pady=10) 
        txt_article = Entry(window_search,width=10)  
        txt_article.pack()
        btn_search = Button(window_search, text="Поиск", command=lambda:[new_button(), clicked_search()])  
        btn_search.pack(pady=5)
        window_search.mainloop() 


def clicked_search():
    res_article = txt_article.get()
    article = str_to_num(res_article)
    response = connect(article)
    response_article = response[0]
    response_name = response[1]
    response_quantity = response[2]
    response_location = response[3]
    
    global lbl_article_found
    global lbl_name
    global lbl_quantity
    global lbl_location
    lbl_article_found = Label(window_search, text='Артикул - %s'%response_article)  
    lbl_article_found.pack()  

    lbl_name = Label(window_search, text='Наименование - %s'%response_name)  
    lbl_name.pack()  

    lbl_quantity = Label(window_search, text='Количество - %s'%response_quantity)  
    lbl_quantity.pack() 

    lbl_location = Label(window_search, text='Местонахождение - %s'%response_location)  
    lbl_location.pack()  

def clicked_search_admin():
    res_article = txt_article.get()
    article = str_to_num(res_article)
    response = connect(article)
    response_article = response[0]
    response_name = response[1]
    response_quantity = response[2]
    response_location = response[3]
    response_supplier = response[4]
    response_date_last_supply = response[5]
    response_date_next_supply = response[6]
    response_time_turnover = response[7]
    global lbl_article_found
    global lbl_name
    global lbl_quantity
    global lbl_location
    global lbl_supplier
    global lbl_date_last_supply
    global lbl_date_next_supply
    global lbl_time_turnover
    lbl_article_found = Label(window_search, text='Артикул - %s'%response_article)  
    lbl_article_found.pack()  

    lbl_name = Label(window_search, text='Наименование - %s'%response_name)  
    lbl_name.pack() 

    lbl_quantity = Label(window_search, text='Количество - %s'%response_quantity)  
    lbl_quantity.pack()  

    lbl_location = Label(window_search, text='Местонахождение - %s'%response_location)  
    lbl_location.pack()

    lbl_supplier = Label(window_search, text='Поставщик - %s'%response_supplier)  
    lbl_supplier.pack()  

    lbl_date_last_supply = Label(window_search, text='Дата последней поставки - %s'%response_date_last_supply)  
    lbl_date_last_supply.pack()  

    lbl_date_next_supply = Label(window_search, text='Дата следующей поставки - %s'%response_date_next_supply)  
    lbl_date_next_supply.pack()  

    lbl_time_turnover = Label(window_search, text='Товарооборот - %s'%response_time_turnover)  
    lbl_time_turnover.pack()

window_auth = Tk()  
window_auth.title("Авторизация")  
window_auth.geometry('400x250')  
lbl_log = Label(window_auth, text="Логин")  
lbl_log.pack(pady=10)  
txt_log = Entry(window_auth,width=10)  
txt_log.pack()

lbl_pass = Label(window_auth, text=" Пароль")  
lbl_pass.pack(pady=10)  
txt_pass = Entry(window_auth,width=10)  
txt_pass.pack() 

btn = Button(window_auth, text="Войти", command=clicked)  
btn.pack()  
window_auth.mainloop()

if __name__ == '__main__':
    connect(article)