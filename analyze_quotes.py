import sqlite3
from unittest import result

conn = sqlite3.connect("quotes.db")
cursor_obj = conn.cursor()

#cursor_obj.execute("""SELECT * FROM authors""")
#results = cursor_obj.fetchall()
#print(results)


#1. return total no of quotations on the wbsite

def get_total_no_of_quotations():
    cursor_obj.execute(""" SELECT COUNT(quote_id) FROM quotes""")
    result = cursor_obj.fetchall()
    count, = result[0]
    return count

total_quotations = get_total_no_of_quotations()
print(total_quotations)

#2. total quotation by author

def get_no_of_quotes_by_author():
    # am taking name as Albert Einstein, we can read any name with input() function
 
    cursor_obj.execute(""" SELECT COUNT(author) FROM authors WHERE author = "Albert Einstein" """)
    result = cursor_obj.fetchall()
    result, = result[0]
    return result

no_of_quotations_by_author = get_no_of_quotes_by_author()
print(no_of_quotations_by_author)

#3.Return Minimum, Maximum, and Average no. of tags on the quotations

def get_min_max_avg_no_of_tags_on_quotatins():
    cursor_obj.execute(""" SELECT MIN(tags_count), MAX(tags_count), avg(tags_count) FROM tags """)
    results = cursor_obj.fetchall()
    results = results[0]
    (min_tags, max_tags, avg_of_tags) = results
    min = "min tags: "+str(min_tags)
    max = "max tags: "+str(max_tags)
    avg = "avg of tags: "+str(avg_of_tags)
    return min,max,avg

result = get_min_max_avg_no_of_tags_on_quotatins()
print(result)

#4.Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes

def get_who_authored_max_num_of_quotations():
    cursor_obj.execute(""" SELECT author, COUNT(author) AS no_of_quotes FROM authors GROUP BY author ORDER BY no_of_quotes DESC LIMIT 5 """)
    result = cursor_obj.fetchall()
    return result

result = get_who_authored_max_num_of_quotations()
print(result)
