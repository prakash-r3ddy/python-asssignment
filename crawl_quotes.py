from webbrowser import get
import requests
from bs4 import BeautifulSoup
import json

def get_each_quote_details(each_quote):
    quote_element=each_quote.find("span",class_="text")
    author_element=each_quote.find("small",class_="author")
    tags_element=each_quote.find_all("a",class_="tag")
    tags_list=[]
    if len(tags_element) > 0:
        for each_tag in tags_element:
            tags_list.append(each_tag.text)
        each_quote_details={"quote":quote_element.text,
            "author":author_element.text,
            "tags":tags_list}
    else:
        each_quote_details={"quote":quote_element.text,
            "author":author_element.text,
        "tags":tags_list}
        
        
            
    return each_quote_details

def get_author_born_details(link):
    details = requests.get(link)
    soup = BeautifulSoup(details.content,"html.parser")
    author_born_date=soup.find("span",class_="author-born-date")
    author_born_location=soup.find("span",class_="author-born-location")
    
    born_details=author_born_date.text+", "+author_born_location.text
    return born_details

def get_authors_details(each_quote):
    author_element=each_quote.find("a",string="(about)")
    link=author_element.get("href")
    author_url_link="http://quotes.toscrape.com"+link
    author_born_details= get_author_born_details(author_url_link)
        
    author_element=each_quote.find("small",class_="author")
    author_name=author_element.text
    authors_details_obj={
            "name":author_name,
            "born":author_born_details,
            "reference":author_url_link
        }
    return authors_details_obj
        
def get_quotes_details(i):
    crawling_data=requests.get("http://quotes.toscrape.com/page/"+str(i)+"/")
    soup = BeautifulSoup(crawling_data.content,"html.parser")
    quotes_details = soup.find_all("div", class_="quote")
    
    quotes_data={
        "quotes":[],
        "authors":[]
    }
    
    for each_quote in quotes_details:
        each_quote_details=get_each_quote_details(each_quote)
        authors_details=get_authors_details(each_quote)
        quotes_data["quotes"].append(each_quote_details)   
        quotes_data["authors"].append(authors_details)
          
    return quotes_data    

all_quotes_data={
    "quotes":[],
    "authors":[]
}

for i in range(1,11):
    quotes_data=get_quotes_details(i)
    all_quotes_data["quotes"].extend(quotes_data["quotes"])
    all_quotes_data["authors"].extend(quotes_data["authors"])
    
json_file=json.dumps(all_quotes_data,indent=4)       

with open("quotes.json", "w") as f:
    json.dump(json_file,f)