from email.quoprimime import quote
from enum import auto
import json
import sqlite3
from unittest import result

def get_auther_id_from_authors_table(author_name,cursor_obj,conn):
    cursor_obj.execute('SELECT author_id FROM authors WHERE author = ? ',author_name)
    author_id = cursor_obj.fetchall()
    author_id, = (author_id[0])
    return author_id

def insert_values_into_quotes_table(cursor_obj,conn,quotes_list):
    length = len(quotes_list)
    id = 0
    for i in range(length):
        quote_obj = quotes_list[i]
        quote = quote_obj["quote"]
        tags_list = quote_obj["tags"]
        author_name = (quote_obj["author"],)
        author_id = get_auther_id_from_authors_table(author_name,cursor_obj,conn)
        id += 1
        cursor_obj.execute("""INSERT INTO quotes VALUES(?,?,?,?)""",(id, quote,len(tags_list),author_id))
    conn.commit()  
      
def insert_values_into_author_table(cursor_obj,conn,authors_list):
    length = len(authors_list)
    id = 0
    for i in range(length):
        author_obj = authors_list[i]
        author_name, born_details, refenrence_link = author_obj["name"],author_obj["born"],author_obj["reference"]
        id +=1
        cursor_obj.execute("""INSERT INTO authors VALUES(?,?,?,?)""",(id,author_name,born_details, refenrence_link))
    conn.commit()    

def get_all_tags_from_each_quote(quotes_list):
    tags_list = []
    for i in range(len(quotes_list)):
        tags_list.extend(quotes_list[i]["tags"])
    return tags_list   
 
def get_unique_tags_from_each_quote(quotes_list):
    unique_tags_list = []
    tags_list = get_all_tags_from_each_quote(quotes_list)
    for each_tag in tags_list:
        if each_tag not in unique_tags_list:
            unique_tags_list.append(each_tag)  
    return unique_tags_list    
    
def insert_values_into_tags_table(cursor_obj,conn,quotes_list):
    unique_tags_list = get_unique_tags_from_each_quote(quotes_list)
    id = 0
    for each_tag in unique_tags_list:
        id += 1
        cursor_obj.execute("""INSERT INTO tags VALUES(?,?)""",(id,each_tag))    
    conn.commit()    

def create_tables(cursor_obj):
    cursor_obj.execute(""" CREATE TABLE quotes(quote_id INT NOT NULL PRIMARY KEY, quote TEXT,no_of_tags_used INT, author_id INT,FOREIGN KEY (author_id) REFERENCES authors(author_id) ON DELETE CASCADE )""")
    cursor_obj.execute(""" CREATE TABLE authors(author_id INT NOT NULL PRIMARY KEY,author TEXT, born TEXT, reference TEXT)""")
    cursor_obj.execute(""" CREATE TABLE tags(tag_id INT NOT NULL PRIMARY KEY,tag TEXT)""")
    cursor_obj.execute(""" CREATE TABLE quote_tags(quote_id INT,tag_id INT, FOREIGN KEY(tag_id) REFERENCES tags(tag_id),
                                                                    FOREIGN KEY(quote_id) REFERENCES quotes(quote_id) ) """)
        
    
def get_tag_id_and_insert_into_qeote_tags_table(quote_id,cursor_obj,tags_list):
    for each_tag in tags_list:
        tag_name = (each_tag,)
        cursor_obj.execute('SELECT tag_id FROM tags WHERE tag = ? ',tag_name)
        tag_id = cursor_obj.fetchall()
        tag_id, = (tag_id[0])
        cursor_obj.execute(""" INSERT INTO quote_tags VALUES(?,?)""",(quote_id,tag_id))
        
    
def insert_values_into_quote_tag_table(cursor_obj,conn,quotes_list):
    id = 0
    for i in range(len(quotes_list)):
        id += 1
        tags_list = quotes_list[i]["tags"]
        if len(tags_list) > 0:
            get_tag_id_and_insert_into_qeote_tags_table(id,cursor_obj,tags_list)
    conn.commit()        

def insert_values_into_tables(cursor_obj,conn,quotes_and_authors_obj):
    insert_values_into_quotes_table(cursor_obj,conn,quotes_and_authors_obj["quotes"])
    insert_values_into_author_table(cursor_obj,conn,quotes_and_authors_obj["authors"])
    insert_values_into_tags_table(cursor_obj,conn,quotes_and_authors_obj["quotes"])
    insert_values_into_quote_tag_table(cursor_obj,conn,quotes_and_authors_obj["quotes"])
    

def create_insert_values_into_tables():
    file_name = "quotes.json"
    with open(file_name,"r", encoding="utf-8") as f:
        quotes_and_authors_obj =json.load(f) 
    authors = quotes_and_authors_obj["authors"]
    conn = sqlite3.connect("quotes.db")
    cursor_obj = conn.cursor()  
    #create_tables(cursor_obj)
    #insert_values_into_tables(cursor_obj,conn,quotes_and_authors_obj)
    
    
    
    #cursor_obj.execute("""DROP TABLE quotes""")
    #cursor_obj.execute("""SELECT (count(quote_id)) as p FROM quote_tags  GROUP BY quote_ida """)
    #results = cursor_obj.fetchall()
    #print(results)

create_insert_values_into_tables()