#!/usr/bin/python
#-*- coding: UTF-8 -*-

import urllib2
import re
import dao
import time
from datetime import datetime
import threading,thread

# 条件变量，用于存放阻塞的线程
cv = threading.Condition()

def httpCrawler(url):
    content = httpRequest(url)
    page = parseHtml(content)
    return page

def httpRequest(url):
    #Request source file
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read()
    return page

def parseHtml(page):
    pattern = re.compile('<a href="http://yue.ifeng.com/news/detail_(.*?)" target="_blank">(.*?)</a>',re.S)
    items = re.findall(pattern,page)
    for item in items:
        print item[0],item[1]
    return items

def savePageList(items):
    #Save source file
    webFile = open('pageList.html','wb')
    titles = ''
    for item in items:
        print item[1],item[0]
        titles = titles + item[0] + item[1]
    webFile.write(titles)
    webFile.close()

def savePage(page):
    #Save source file
    webFile = open('pageList.html','wb')
    webFile.write(page)
    webFile.close()

def now():
    cur = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print cur
    return cur

def cond_wait(cond,mutex):
    #cond.acquire()
    #current_thread = threading.current_thread()
    #threads.append(current_thread)   
    #cond.release()
    
    #释放、阻塞等待、被唤醒获取锁
    mutex.release()
    mutex.wait()    
    mutex.acquire()

def cond_signal(cond):
    cond.acquire() 
    if len(threads) > 0:
        thread_nofify = threads.pop()
    cond.release()

def run():
    while True:
        print "开始处理任务"
        task = dao.select(state=0)       
        cv.acquire()
        while task == None:
            cv.wait()
        cv.release()
        ret = dao.update(state=1, update_time=now(), id=task.id)
        if ret == 0:
            print "任务已经被处理，直接跳出循环"
            continue
        page = httpCrawler(task.link)   
        if task.type == 0:
            print "处理列表任务...."
            cv.acquire()
            cv.notify()
            cv.release()
            dao.update(state=2, update_time=now(), id=task.id)
        if task.type == 1:
	    print "抓页面...."    
            ret = dao.update(state=2, update_time=now(), id=task.id)
        print "任务完成"

if __name__ == '__main__':
    thread.start_new_thread(run())
    thread.start_new_thread(run())
