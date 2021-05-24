# File to store info about all variables related to application configuration

"""
link           -  to define the sourceLink
Links          -  MongoDB collection to store all data
Links['link']  -  field name to store URL addresses in database
Links['CreatedAt'] - field name to store date and time of scrapped links
sourceLink     -  to store extracted link from database
parse_content  -  to store content parsed using BeutifulSoup 
criteria       -  it defines the filter(condition) used to crawled time of links
count          -  to count no of links scraped in a cycle

validateURL()   - a function to validate an URL using try & catch mechanism
scrapeCycle()   - a function to execute one scrape cycle
isCrawled()     - a function to check whether link already exists in database
time24HoursAgo() - a function to count time at 24 hours ago

"""
