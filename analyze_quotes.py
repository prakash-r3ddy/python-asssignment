import sqlite3
from unittest import result

#1. return total no of quotations on the wbsite

def get_total_no_of_quotations(cursor_obj):
    cursor_obj.execute(""" SELECT COUNT(quote_id) FROM quotes""")
    result = cursor_obj.fetchall()
    count, = result[0]
    print("Totl no of quotations: "+str(count))

#2. total quotation by author

def get_no_of_quotes_by_author(cursor_obj):
    user_input = input("ENTER AUTHOR NAME: ")
    author_name = (user_input,)
    cursor_obj.execute(""" SELECT COUNT(quote_id) FROM quotes INNER JOIN
                                authors on quotes.author_id = authors.author_id WHERE authors.author LIKE ? """, author_name)
    result = cursor_obj.fetchall()
    total_quotes, = result[0]
    print("Total Quotations by "+user_input+" are: "+str(total_quotes))

#3.Return Minimum, Maximum, and Average no. of tags on the quotations

def get_min_max_avg_no_of_tags_on_quotatins(cursor_obj):
    cursor_obj.execute(""" SELECT MIN(no_of_tags_used),MAX(no_of_tags_used),AVG(no_of_tags_used) FROM quotes """)
    results = cursor_obj.fetchall()
    results = results[0]
    (min_tags, max_tags, avg_of_tags) = results
    min = "  min tags: "+str(min_tags)
    max = "  max tags: "+str(max_tags)
    avg = "  avg of tags: "+str(avg_of_tags)
    print(min,max,avg)

#4.Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes

def get_who_authored_max_num_of_quotations(cursor_obj):
    user_input = int(input("ENTER NUMBER: "))
    number = (user_input,)
    cursor_obj.execute(""" SELECT author, COUNT(author) AS no_of_quotes FROM authors INNER JOIN quotes ON 
                       authors.author_id = quotes.author_id GROUP BY author ORDER BY no_of_quotes DESC LIMIT ? """,number)
    result = cursor_obj.fetchall()
    print(result)

def get_answers_for_given_questions():
    conn = sqlite3.connect("quotes.db")
    cursor_obj = conn.cursor()
    get_total_no_of_quotations(cursor_obj)
    get_no_of_quotes_by_author(cursor_obj)
    get_min_max_avg_no_of_tags_on_quotatins(cursor_obj)
    get_who_authored_max_num_of_quotations(cursor_obj)
""
get_answers_for_given_questions()