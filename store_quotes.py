from email.quoprimime import quote
from enum import auto
import json
import sqlite3
from unittest import result

def insert_values_into_quotes_table(cursor_obj,conn,quotes_data):
    length = len(quotes_data["quotes"])
    id = 0
    for i in range(length):
        quote_list = quotes_data["quotes"][i]
        quote_obj = dict(quote_list)
        quote = quote_obj["quote"]
        author_name = (quote_obj["author"],)
        tags_count = len(quote_obj["tags"])
        cursor_obj.execute('SELECT author_id FROM authors WHERE author = ? ',author_name)
        author_id = cursor_obj.fetchall()
        author_id, = (author_id[0])
        id += 1
        cursor_obj.execute("""INSERT INTO quotes VALUES(?,?,?,?)""",(id, quote,tags_count,author_id))
    conn.commit()  
      
def insert_values_into_author_table(cursor_obj,conn,quotes_data):
    unique_authors_list = []
    for i in quotes_data["authors"]:
        if i not in unique_authors_list:
            unique_authors_list.append(i)
    length = len(unique_authors_list)
    id = 0
    for i in range(length):
        author_list = unique_authors_list[i]
        author_obj = dict(author_list)
        author_name = author_obj["name"]
        born_details = author_obj["born"]
        refenrence_link = author_obj["reference"]
        id +=1
        cursor_obj.execute("""INSERT INTO authors VALUES(?,?,?,?)""",(id,author_name,born_details, refenrence_link))
    conn.commit()    
    
def insert_values_into_tags_table(cursor_obj,conn,quotes_data):
    length = len(quotes_data["quotes"])
    id = 0
    for i in range(length):
        quote = quotes_data["quotes"][i]
        quote_obj = dict(quote)
        quote_tags = quote_obj["tags"]
        tags_count = len(quote_tags)
        id += 1
        for j in range(tags_count):
            tag = quote_tags[j]
            print(id,tag,id)
            cursor_obj.execute("""INSERT INTO tags VALUES(?,?,?)""",(id,tag,id))    
    conn.commit()    

def create_tables(cursor_obj):
    cursor_obj.execute(""" CREATE TABLE quotes(quote_id INT NOT NULL PRIMARY KEY, quote TEXT,no_of_tags_used INT, author_id INT,FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE )""")
    cursor_obj.execute(""" CREATE TABLE authors(author_id INT NOT NULL PRIMARY KEY,author TEXT, born TEXT, reference TEXT)""")
    cursor_obj.execute(""" CREATE TABLE tags(tag_id INT,tag TEXT, quote_id INT, FOREIGN KEY (quote_id) REFERENCES quotes(quote_id) ON DELETE CASCADE  )""")


def insert_values_into_tables(cursor_obj,conn,quotes_data):
    insert_values_into_quotes_table(cursor_obj,conn,quotes_data)
    insert_values_into_author_table(cursor_obj,conn,quotes_data)
    insert_values_into_tags_table(cursor_obj,conn,quotes_data)
    return

def create_insert_values_into_tables():
    file_name = "quotes.json"
    with open(file_name,"r", encoding="utf-8") as f:
        data=json.load(f)
    quotes_data=json.loads(data) 
    authors = quotes_data["authors"]
    
    conn = sqlite3.connect("quotes.db")
    cursor_obj = conn.cursor()
      
    #create_tables(cursor_obj)
    #insert_values_into_tables(cursor_obj,conn,quotes_data)
    
    #cursor_obj.execute("""DROP TABLE quotes""")
    #cursor_obj.execute("""SELECT count(*) AS total FROM tags """)
    #results = cursor_obj.fetchall()
    #print(results)

create_insert_values_into_tables()