import requests
from bs4 import BeautifulSoup
import validators
from pymongo import MongoClient

URL = "https://flinkhub.com"                    #define the URL

client = MongoClient()                          #instablish a connection
db = client["Crawler"]                          #define the collection
db.Links.insert_one( {"link":URL} )             #insert root URL in database

req = requests.get(URL)                         #send request to server and server will send 'response HTLML' 

parse_content = BeautifulSoup(req.text, 'html5lib')     #parse 'response HTML' using BeautifulSoup

for i in parse_content.find_all('a', href=True):        #extract <a> tag from parse content
    if validators.url(i['href']):                       #check for valid URL
        db.Links.insert_one({"link":i['href']})         #if URL is valid insert it into database
