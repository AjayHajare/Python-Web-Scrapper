import requests
from bs4 import BeautifulSoup
import validators
from pymongo import MongoClient


client = MongoClient()                                                      #instablish a connection
db = client["Crawler"]                                                      #define the collection


#function to check whether link already exists:
def alreadyExists(URL):
    if db.Links.count_documents({"link":URL}, limit = 1) > 0:                   #limit=1 means it will search for function and as soon as it find result first time, it will return
        return True
    else:
        return False
    
    
def main():
        URL = "https://flinkhub.com/"                                           #define the URL

        if(not alreadyExists(URL)):
                db.Links.insert_one( {"link":URL} )                             #insert root URL in database

        criteria = {"$and": [{"date": {"$gte": time24HoursAgo() }} ]}           #'criteria' variable is a 'filter' to fetch all links with date ($gte)greater than 'days_back'

        #db.Links.delete_many({})

        for _ in range(2):
                req = requests.get(URL)                                         #send request to server and server will send 'response HTLML' 

                parse_content = BeautifulSoup(req.text, 'html5lib')             #parse 'response HTML' using BeautifulSoup

                for i in parse_content.find_all('a', href=True):                #extract <a> tag from parse content
                    if ( validators.url(i['href']) and  not alreadyExists(i['href']) ):                                  #check for valid URL and check whether URL is already present in database
                        db.Links.insert_one({"link":i['href'], "date":datetime.today().replace(microsecond=0) })         #if URL is valid and not present in database, insert link and time into database

        
                
if __name__ == '__main__' :
        main()
