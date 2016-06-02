

#who = sys.argv[1]
#a=1
#b=2
#c=who
#print a+":"+b+":"+who

import requests
import datetime
import re
import sys
from bs4 import BeautifulSoup

url = sys.argv[1]
url = url + 'issues'
#print url


# url = '	' + 'issues'
# url = 'https://github.com/Shippable/cexec/' + 'issues'

r = requests.get(url)
soup = BeautifulSoup(r.text)

#  Retrieve all the page no where issues are listed
import urlparse
pages = {}
BASE_URL = 'https://github.com'

# This will generate a dictionary with the page index as key and url as the value
for all_links in soup.findAll({'div'}, {'class': 'pagination'}):
    for link in all_links.findAll('a'):
        page_index = str(link.extract().text)
        if page_index not in pages.keys() and page_index != 'Next' :
            pages[page_index] = urlparse.urljoin(BASE_URL, link.attrs['href'])
    break

# for page, link in sorted(pages.items()):
#     print page, link

# Scrap the first Issues page


issue_timestamp_dict = {}
def crawler(soup):
    for value in soup.findAll({'span'},{'class' : 'issue-meta-section opened-by'}):
        issue_no = re.search(r'(#\d+)',str(value.extract().text),re.M|re.I).group()
    
#     Store all datetime stamp for every listed issue in the current page [page 1] to a dictionary
        for time in value.findAll('relative-time'): # this loop runs for only one iteration
#         Clean the timestamp from this '2016-06-01T04:39:22Z' to this '2016-06-01 04:39:22'
#         and store it as datetime object so it could be operated upon
            date = time.get('datetime').strip('Z').split('T')
            date = datetime.datetime.strptime(' '.join(date), '%Y-%m-%d %H:%M:%S')

#         If the dictionary is empty create a new index key and add current date as its value
            if issue_no not in issue_timestamp_dict.keys():
                issue_timestamp_dict[issue_no] = date
#             print issue_no, date
            break
    return issue_timestamp_dict

crawler(soup)

# Scrap the other pages (if exists)
# for page, link in sorted(pages.items()):
#     print page, link
if bool(pages): # if other pages exists, scrap them too
    for p_link in sorted(pages.values()):
        req = requests.get(p_link)
        soup = BeautifulSoup(req.text)
        # call the crawler function with the BeautifulSoup object
        # and it will populate the dictionary items with new issue_no
        # and timestamp values
        crawler(soup)

from operator import itemgetter

# - Number of open issues that were opened in the last 24 hours
count_24 = 0
# - Number of open issues that were opened more than 24 hours ago but less than 7 days ago
count_24_7 = 0
# - Number of open issues that were opened more than 7 days ago 
count_m7 = 0

# reverse sort the dictionary according to its value and display the result
for k,v in sorted(issue_timestamp_dict.items(), reverse=True, key=itemgetter(1)):
    
    # Geting Present time (Now) in proper format 
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    present_time = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
    
#     Computing the difference b/w present time and timestamp value
    time_diff = present_time - v 
    if time_diff.days == 0:
        count_24 += 1
#         print 'open issues in the last 24 hours:', k, time_diff
    elif time_diff.days in xrange(1,7):
        count_24_7 += 1
#         print 'open issues in the last 24 hours but less than 7 days:', k, time_diff
    elif time_diff.days >= 7:
        count_m7 += 1

open_issue_count = len(issue_timestamp_dict)
# print 'Open Issues: ', open_issue_count
# print 'open issues in the last 24 hours:',count_24
# print 'open issues in the last 24 hours but less than 7 days:',count_24_7
# print 'open issues that were opened more than 7 days ago:',count_m7

print str(open_issue_count) + ':' + str(count_24) +':' + str(count_24_7) + ':' + str(count_m7)
