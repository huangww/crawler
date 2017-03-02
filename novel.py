#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
import thread
import chardet
import smtplib
from email.mime.text import MIMEText

class NovelSpider():
    """Novel spider class, used to get updated novel chapters."""
    def __init__(self):
        # super(NovelSpider, self).__init__()
        self.pages = []
        self.page = 1
        self.flag = True
        self.url = "http://zetianjixiaoshuo.com"

    def openUrl(self, url):
        """ Open the url use Mozilla agent

        :url: the url to open
        :returns: the unicode page of the url

        """
        userAgent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : userAgent }
        req = urllib2.Request(url, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()

        # convert the page to uicode utf-8 page
        charset = chardet.detect(myPage)
        charset = charset['encoding']
        if charset == 'utf-8' or charset == 'UTF-8':
            myPage = myPage
        else:
            myPage = myPage.decode('gb2312','ignore').encode('utf-8')
        unicodePage = myPage.decode('utf-8')
        return unicodePage
        
    def getPage(self):
        """ get the newest chapter of the novel
        :returns: the dict of page {'title':title, 'content':content}

        """
        unicodePage = self.openUrl(self.url)
        # find the url of the newst chapter first
        try:
            link = re.search('<div.*?class="novel">(.*?)</div>', unicodePage, re.S)
            link = link.group(1)
            urlList= re.findall(u'<a.*?href="(.*?)".*?>(.*?)</a>', link, re.S)
            newestUrl = urlList[1][0]
        except Exception as e:
            print "Fail to get link of the newest chapter."
            print e
            return False
        unicodePage = self.openUrl(self.url+newestUrl)

        # try to find the title
        try:
            myTitle = re.search('<h1>(.*?)</h1>', unicodePage, re.S)
            myTitle = myTitle.group(1)
        except Exception as e:
            print 'Title is changed, please try it again.'
            print e
            return False

        # try to get the content of the chapter
        try:
            # myContent = re.search('<div.*?id="content">(.*?)</div>', unicodePage, re.S)
            contentList = re.findall('<p>(.*?)</p>', unicodePage, re.S)

            myContent = ''
            for content in contentList:
                myContent = myContent + content 
        except Exception as e:
            print 'Content is changed, please redo the analysis.'
            print e
            return False

        myContent = myContent.replace("<br />", "\n")
        myContent = myContent.replace("&nbsp", "")
        myContent = myContent.replace(" ", " ")

        # store the chapter use a dict
        onePage = {'title': myTitle, 'content': myContent}
        return onePage
                

    def loadPage(self):
        """ Load the page and set the flag to false if not success
        :returns: TODO

        """
        while self.flag:
           if len(self.pages) < 1:
               try:
                   myPage = self.getPage()
                   if myPage == False:
                       print "Fail to get the newest chapter."
                       self.flag = False
                   self.pages.append(myPage)
               except Exception as e:
                   print "Cannot connect to the webpage."
                   self.flag = False
    
    def showPage(self, currentPage):
        """ Print the page to the screen

        :currentPage: current loaded page
        :returns: TODO

        """
        print currentPage['title']
        print currentPage['content']
        print '\n'
        userInput = raw_input("Type 'quit' to quit!")
        if userInput == 'quit':
           self.flag = False
        print '\n'

    def emailPage(self, newPage):
        """ Get the page and send to the email address
        :newPage: the page to be emailed
        :returns: TODO

        """
        print "Sending the email..."
        msg = MIMEText(newPage['title'] + '\n' + newPage['content'], 'plain', 'utf-8')
        msg['Subject'] = 'Novel update'
        msg['From'] = 'huangww87@gmail.com'
        msg['To'] = 'huangww87@gmail.com'

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        print "Please input you password:"
        password = raw_input()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print "Email sent out."
        userInput = raw_input("Type 'quit' to quit: ")
        if userInput == 'quit':
           self.flag = False
        


    def start(self):
        """ Start to read the novel
        :returns: TODO

        """
        print u'Loading...'

        thread.start_new_thread(self.loadPage, ())

        # newPage = self.pages[self.page-1]
        # self.showPage(newPage)
        while self.flag:
            if self.page <= len(self.pages):
                newPage = self.pages[self.page-1]
                # self.showPage(newPage)
                self.emailPage(newPage)
                self.page += 1

def main():
    """Define the interface for the program 
    :returns: TODO

    """
    # Interface the the program
    print u"""
    ----------------------------------------------
        Program: Novel Spider
        Version: 1.0
        Author: Wallen
        Date: 2017-03-01
        Language: Python 2.7
        Features: Get the newest novel chapter
    ----------------------------------------------
    """

    myNovel = NovelSpider()
    myNovel.start()

if __name__ == "__main__":
    main()

