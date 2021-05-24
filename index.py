import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
from datetime import datetime, timedelta
import sys
from concurrent.futures import ThreadPoolExecutor

client = MongoClient()                                              #instablish a MongoDB connection
db = client["Crawler"]                                              #define the MongoDB collection



#function to count time at 24 hours ago
def time24HoursAgo() :
        today = datetime.today()                                    #it gives todays date and time
        BackTo24Hours = today - timedelta(days=1)                   #it calculates time for 24 hours ago & stores it in 'days_back' variable
        return BackTo24Hours                                        #return datetime


        
#function to check whether link already exists
def isCrawled(sourceLink):
    criteria = { '$and' : [{"link":sourceLink},{"createdAt": {"$gte": time24HoursAgo()}}] }     # '$and' operator joins two or more queries with a logical AND and returns the documents that match all the conditions.
    if (db.Links.count_documents(criteria) > 0) :                                               # find documents with given link and created time is less than24 hours
        return True
    else :
        return False


#validate an URL using try & catch mechanism
def validateURL(sourceLink) :
    try:
        response = requests.get(sourceLink)
        return True
    except:
        return False

    

#function defined to execute one scrape cycle
def scrapeCycle() :          
        for l in db.Links.find():
            count = 0                                                                   #'count' is defined to count no of links scraped in a cycle
            
            sourceLink = l['link']
            response = requests.get(sourceLink)                                         #send request to server and server will send 'response HTLML'
        
            with open('HTMLresponse/resp.html', 'wb') as f:                             #save the HTML response on the local disk space 
                f.write(response.content)                                  
        
            parse_content = BeautifulSoup(response.text, 'html5lib')                    #parse 'response HTML' using BeautifulSoup

            for i in parse_content.find_all('a', href=True):                            #extract <a> tag from parse content
                if ( validateURL(i['href']) and  not isCrawled(i['href']) ):                                              #check for valid URL and check whether URL is already present in database
                    db.Links.insert_one({"link":i['href'], "createdAt":datetime.today().replace(microsecond=0) })         #if URL is valid and not present in database, insert link and time into database
                    count+=1
                
            if (count==0):
                print("All links crawled")
    
            if db.Links.count_documents({}) >= 5000:
                print("Maximum limit reached")

            
        time.sleep(5)                                                                #it will make process sleep for 5 seconds


#main() function to start execution
if __name__ == '__main__' :
        link = "https://flinkhub.com"                                                #define the sourceLink

        if( validateURL(link) ):                                                     #if the sourceLink is valid, then insert it in database
                db.Links.insert_one( {"link":link, "createdAt":datetime.today().replace(microsecond=0) } )                     
        else :                                                                       #if the sourceLink is invalid, then exit
                print("Please enter a valid URL")
                sys.exit()

        while True:        
                with ThreadPoolExecutor(max_workers = 5) as executor:                        #ThreadPoolExecutor is library in python which is used to implement multithreading
                    executor.submit(scrapeCycle)                                             #call to function 'scrapeCycle()'
        
        
