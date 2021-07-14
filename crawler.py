#!/usr/bin/python3
# -*- coding:utf-8 -*-

import queue
from urllib3 import ProxyManager, make_headers
import re
from datetime import datetime
import dao
from task_model import Task
from bloom_filter import BloomFilter

def store(url,title,tag):
    task = Task(id=None,priority=0,type=1,state=0,link=url,\
                start_time=None,end_time=None,title = title,tag = "",ctime = now(),utime = now())
    dao.insert(task)

def httpRequest(url):
    #Request source file
    proxy = ProxyManager("http://127.0.0.1:1087")
    resp = proxy.request("GET", url)
    page = resp.data.decode("utf-8")
    return page

def extract_urls(url):
    page = httpRequest(url)
    pattern = re.compile('<a href="(.*?)" class="topic-link">(.*?)</a>',re.A)
    items = re.findall(pattern,page)
    urls = []
    for item in items:
        url = "https://www.v2ex.com" + item[0].split("#")[0]
        title = item[1]
        # print(title)
        tag_pattern = re.compile('\[.*?\]',re.A)
        tag = re.findall(tag_pattern,title)
        # print("tag:"+str(tag))
        store(url,title,tag)
        urls.append(url)
    return urls

def now():
    # cur = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur = datetime.now().timestamp() * 1000
    return cur

def main():
    page_start_index = 1
    page_end_index =50
    url_queue  = queue.Queue()
    
    for i in range(page_start_index,page_end_index+1):
        inital_page = "https://www.v2ex.com/go/jobs?p=" + str(i)
        filter = BloomFilter()
        filter.add(inital_page)  
        url_queue.put(inital_page)

    while(True and not url_queue.empty()):
        urls = []
        current_url = url_queue.get() #取队列第一个元素
        try:
	        print(current_url)
	        urls = extract_urls(current_url) #抽取页面中的链接
        except Exception as e:
            print("Error extract_urls")
            print(e)
        if urls:
            for url in urls:
                if not filter.notcontains(url):
                    url_queue.put(url)


if __name__ == "__main__":
    main()

