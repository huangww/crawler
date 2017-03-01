#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import thread
import chardet

class NovelSpider():
    """Novel spider class, used to get updated novel chapters."""
    def __init__(self, arg):
        super(NovelSpider, self).__init__()
        self.arg = arg
        self.pages = []
        self.page = 1
        self.flag = True
        self.url = "http://zetianjixiaoshuo.com"

    def getChapter(self):
        """ get one chapter of the novel
        :returns: TODO

        """
        myUrl = self.url
        userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : userAgent }
        req = urllib2.Request(myUrl, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()

        charset = chardet.detect(myPage)
        charset = charset['encoding']
        if charset == 'utf-8' or charset == 'UTF-8':
            myPage = myPage
        else:
            myPage = myPage.decode('gb2312','ignore').encode('utf-8')
        unicodePage = myPage.decode('utf-8')

        # try to find the match of id = "content" 
        try:
            # try to find the title
            myTitle = re.search('<h1>(.*?)</h1>', unicodePage, re.S)
            myTitle = myTitle.group(1)
        except Exception as e:
            print 'Title is changed, please try it again.'
            return False

        try:
            # try to get the content of the chapter
            myContent = re.search('<div.*?id="content">(.*?)</div>', unicodepage, re.S)
            myContent = myContent.group(1)
        except Exception as e:
            print 'Content is changed, please re do the analysis.'
            return False

        myContent = myContent.replace("<br />", "\n")
        myContent = myContent.replace("&nbsp", "")
        myContent = myContent.replace(" ", " ")

        # store the chapter use a dict
        oneChapter = {'title': myTitle, 'content': myContent)

        try:
            pass
        except Exception as e:
            raise e
        
        

