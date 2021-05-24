import requests
from bs4 import BeautifulSoup
import validators
from pymongo import MongoClient
import time
from datetime import datetime, timedelta

client = MongoClient()                                                      #instablish a connection
db = client["Crawler"]                                                      #define the collection


#function to check whether link already exists:
def alreadyExists(URL):
    if db.Links.count_documents({"link":URL}, limit = 1) > 0:                   #limit=1 means it will search for function and as soon as it find result first time, it will return
        return True
    else:
        return False
    
#function to count time at 24 hours ago
def time24HoursAgo() :
        today = datetime.today()                                #it gives todays date and time
        BackTo24Hours = today - timedelta(days=1)                 #it calculates time for 24 hours ago & stores it in 'days_back' variable
        return BackTo24Hours                                      #return datetime

#function validate an URL using try & catch mechanism
def validateURL(sourceLink) :
    try:
        response = requests.get(sourceLink)
        return True
    except:
        return False

#function to perform scrapping
def scrapeCycle() :          
        for l in db.Links.find():
            count = 0                                                             #'count' is defined to count no of links scraped in a cycle
            
            sourceLink = l['link']
            response = requests.get(sourceLink)                                  #send request to server and server will send 'response HTLML'
        
            with open('HTMLresponse/resp.txt', 'wb') as f:                        #save the HTML response on the local disk space 
                f.write(response.content)                                  
        
            parse_content = BeautifulSoup(response.text, 'html5lib')             #parse 'response HTML' using BeautifulSoup

            for i in parse_content.find_all('a', href=True):                      #extract <a> tag from parse content
                if ( validateURL(i['href']) and  not isCrawled(i['href']) ):                                  #check for valid URL and check whether URL is already present in database
                    db.Links.insert_one({"link":i['href'], "createdAt":datetime.today().replace(microsecond=0) })         #if URL is valid and not present in database, insert link and time into database
                    count+=1
                
            if (count==0):
                print("All links crawled")
    
            if db.Links.count_documents({}) >= 5000:
                print("Maximum limit reached")
 
        time.sleep(5)                                                                                           #it will make process sleep for 5 seconds

if __name__ == '__main__' :
        link = "https://github.com"                                                                             #define the sourceLink

        if( validateURL(link) ):                                                                                #if the sourceLink is valid, then insert it in database
                db.Links.insert_one( {"link":link, "createdAt":datetime.today().replace(microsecond=0) } )                     
        else :                                                                                                  #if the sourceLink is invalid, then exit
                print("Please enter a valid URL")
                sys.exit()

        while True:
                scrapeCycle()
 
