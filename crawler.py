#!/usr/bin/python
# -*- coding:utf-8 -*-

import Queue
import urllib2
import re
import MySQLdb

def store(url):
    page = httpRequest(url)
    #Save source file
    webFile = open('pageList.html','wb')
    webFile.write(page)
    webFile.close()

def httpRequest(url):
    #Request source file
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read()
    return page

def extract_urls(url):
    page = httpRequest(url)
    pattern = re.compile('<a href="(.*?)" target="_blank">(.*?)</a>',re.S)
    items = re.findall(pattern,page)
    for item in items:
        print item[0],item[1]
    return items

inital_page = "http://www.thepaper.cn/channel_25950"

url_queue  = Queue.Queue()
seen = set()

seen.add(inital_page)
url_queue.put(inital_page)

while(True):
    current_url = url_queue.get()
    print current_url
    store(current_url)
    urls = extract_urls(current_url)
    for next_url in urls:
        if next_url not in seen:
            seen.add(next_url)
            url_queue.put(next_url)

