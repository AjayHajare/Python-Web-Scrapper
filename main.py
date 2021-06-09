from cfg import root_URL
from database import getLinks, insertLinkInDatabase
from crawler import scrapeCycle, getResponse, saveFile
from concurrent.futures import ThreadPoolExecutor
import requests

if __name__ == "__main__":
    response = getResponse(root_URL)

    if response.status_code==200:
        insertLinkInDatabase(root_URL, '', response, saveFile(root_URL), '')      
    else:
        print("Please enter valid URL")

    while True:     
        try :
            pendingLinks = getLinks()
            with ThreadPoolExecutor(max_workers = 5) as executor:                        #ThreadPoolExecutor is library in python which is used to implement multithreading
                executor.map(scrapeCycle,pendingLinks)                                   #call to function 'scrapeCycle()'
                
        except Exception as error :
            print(error)
    
