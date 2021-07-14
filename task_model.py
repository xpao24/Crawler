#!/usr/bin/python 
# -*- encoding:utf-8 -*-

class Task(object):

    def __init__(self,id,priority,type,state,link,start_time,end_time,title,tag,ctime,utime):
        self.id = id
        self.priority = priority
        self.type = type
        self.state = state
        self.link = link
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.tag = tag
        self.ctime = ctime
        self.utime = utime

