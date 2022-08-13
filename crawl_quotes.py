from webbrowser import get
import requests
from bs4 import BeautifulSoup
import json

def get_tags_list_from_tags_element(tags_element):
    tags_list = []
    if tags_element == None:
        return None
    else:
        for each_tag in tags_element:
            tags_list.append(each_tag.text)
        return tags_list  
    
def get_each_quote_text(each_quote):
    quote_element = each_quote.find("span",class_="text")      
    quote = quote_element.text
    sliced_quote = quote[1:len(quote)-1]
    return sliced_quote

def get_each_quote_details(each_quote):
    quote_text = get_each_quote_text(each_quote)
    author_element=each_quote.find("small",class_="author")
    tags_element=each_quote.find_all("a",class_="tag")
    tags_list = get_tags_list_from_tags_element(tags_element)
    each_quote_details={"quote":quote_text,"author":author_element.text,"tags":tags_list}            
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
        
def get_quotes_and_author_details(url):
    crawling_data=requests.get(url)
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

def get_next_page_link_if_their(website_url):
    data =requests.get(website_url)
    soup = BeautifulSoup(data.content,"html.parser")
    next_button= soup.find("li", class_="next")
    if next_button == None:
        return None
    else:
        anchor_elemenet = next_button.find("a")
        button_link = anchor_elemenet.get("href")
        website_url = "http://quotes.toscrape.com"+button_link
        return website_url

def get_crawling_data_from_website():
    quotes_and_authors_obj={
    "quotes":[],
    "authors":[]
    }
    website_url = "http://quotes.toscrape.com/"
    while True:
        quotes_data = get_quotes_and_author_details(website_url)
        quotes_and_authors_obj["quotes"].extend(quotes_data["quotes"])
        quotes_and_authors_obj["authors"].extend(quotes_data["authors"])
        next_page_url = get_next_page_link_if_their(website_url)
        if next_page_url == None:
            return quotes_and_authors_obj
        else:
            website_url = next_page_url
            
def get_unique_authors_list(authors_list):
    unique_list = []
    for each_author in authors_list:
        if each_author not in unique_list:
            unique_list.append(each_author)
    return unique_list        
            
def get_crawled_data_and_add_it_to_json_file():
    quotes_and_authors_obj = get_crawling_data_from_website()    
    uniq_authors_list = get_unique_authors_list(quotes_and_authors_obj["authors"])
    quotes_and_authors_obj["authors"] = uniq_authors_list
    with open("quotes.json", "w") as f:
        json.dump(quotes_and_authors_obj, f, indent = 2)    

        
get_crawled_data_and_add_it_to_json_file()
