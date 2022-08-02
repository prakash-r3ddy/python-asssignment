from email.quoprimime import quote
import json
import sqlite3
from unittest import result

file_name = "quotes.json"
with open(file_name,"r", encoding="utf-8") as f:
    data=json.load(f)
quotes_data=json.loads(data)

conn = sqlite3.connect("quotes.db")
cursor_obj = conn.cursor()

#cursor_obj.execute(""" CREATE TABLE quotes(quote_id INT, quote TEXT)""")

#cursor_obj.execute(""" CREATE TABLE authors(author_id INT,quote_id INT, author TEXT)""")

#cursor_obj.execute(""" CREATE TABLE tags(tag_id INT,quote_id INT, tag TEXT, tags_count INT)""")

def insert_values_into_quotes_table():
    length = len(quotes_data["quotes"])
    id = 0
    for i in range(length):
        quote_list = quotes_data["quotes"][i]
        quote_obj = dict(quote_list)
        quote = quote_obj["quote"]
        id += 1
        cursor_obj.execute("""INSERT INTO quotes VALUES(?,?)""",(id, quote))
    conn.commit()  
      
def insert_values_into_author_table():
    length = len(quotes_data["quotes"])
    id = 0
    for i in range(length):
        author_list = quotes_data["quotes"][i]
        author_obj = dict(author_list)
        author_name = author_obj["author"]
        id +=1
        cursor_obj.execute("""INSERT INTO authors VALUES(?,?,?)""",(id,id,author_name))
    conn.commit()    
    
def insert_values_into_tags_table():
    length = len(quotes_data["quotes"])
    id = 0
    for i in range(length):
        tags = quotes_data["quotes"][i]
        tags_obj = dict(tags)
        quote_tags = tags_obj["tags"]
        tags_count = len(quote_tags)
        id += 1
        tag_names = ",".join(quote_tags)
        cursor_obj.execute("""INSERT INTO tags VALUES(?,?,?,?)""",(id,id,tag_names,tags_count))
    conn.commit()    

#insert_values_into_quotes_table()
#insert_values_into_author_table()
#insert_values_into_tags_table()

#cursor_obj.execute("""DROP TABLE authors""")

#cursor_obj.execute("""SELECT * FROM quotes""")
#cursor_obj.execute("""SELECT * FROM authors""")

#results = cursor_obj.fetchall()
#print(results)