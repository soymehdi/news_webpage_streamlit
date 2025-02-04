import streamlit as st
from bs4 import BeautifulSoup
import sqlite3, threading, requests
##################

def clean_database():
    with sqlite3.connect("digi.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM digi") 
        conn.commit()
    with sqlite3.connect("api.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM api") 
        conn.commit()
#----------------------------------------

def api_database_filling():
    conn = sqlite3.connect('api.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS api
                 (userid TEXT, id TEXT, title TEXT, body TEXT)''')

    for i in range(1, 11):
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{i}")
        element = response.json()
        userid = element['userId']
        iid = element['id']
        title = element['title']
        body = element['body']
        c.execute("INSERT INTO api (userid, id, title, body) VALUES (?, ?, ?, ?)", (userid, iid, title, body))

    conn.commit()
    conn.close()
#----------------------------------------

def digi_datbase_filling():
    conn = sqlite3.connect('digi.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS digi
                (text TEXT)''')

    response = requests.get("https://www.digiato.com/")
    soup = BeautifulSoup(response.text, 'html.parser')

    news = soup.find_all("a", class_="rowCard__title")
    for i in news:
        texx = i.text
        c.execute("INSERT INTO digi (text) VALUES (?)", (texx ,))

    conn.commit()
    conn.close()
#----------------------------------------

def reading_api_db():
    with sqlite3.connect('api.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM api")
        data = c.fetchall()
        c.close()
        return data
#----------------------------------------

def reading_digi_db():
    with sqlite3.connect('digi.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM digi")
        data = c.fetchall()
        c.close()
        return data
#----------------------------------------

t1 = threading.Thread(target=digi_datbase_filling) 
t2 = threading.Thread(target=api_database_filling)
t3 =threading.Thread(target=clean_database)

st.write("N.E.W.S WebPage :globe_with_meridians:")
with st.spinner("Processing..."):
    t3.start()
    t1.start()
    t2.start()
    t3.join()
    t1.join()
    t2.join()

api_news_list = reading_api_db()
for element in api_news_list:
    st.write(f"{element[1]}: ")
    st.write(element[3])

i = 11
digi_news_list = reading_digi_db()
for element in digi_news_list:
    st.write(f"{i}:")
    i += 1
    st.write(element[0])






