"""
This is a script used to grab the on-line novel update chapter
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import thread
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


class NovelSpider(object):
    """ Novel spider class, used to get updated novel chapters."""
    def __init__(self):
        super(NovelSpider, self).__init__()
        self.pages = []
        self.page_number = 1
        self.flag = True
        self.url = "http://zetianjixiaoshuo.com"

    @staticmethod
    def open_url(url):
        """ Open the url use Mozilla agent

        :url: the url to open
        :returns: the unicode page of the url

        """
        agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
        headers = {'User-Agent' : agent}
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        page = response.read()
        return page


    def get_update_url(self):
        """ Get the url of the newest chapter
        :returns: url, string

        """
        page = self.open_url(self.url)
        soup = BeautifulSoup(page, 'lxml')
        newest_url = ''
        try:
            for tag in soup.find("span", class_="fl"):
                newest_url = tag.get('href')
        except Exception as err:
            raise err
        newest_url = self.url + newest_url
        return newest_url


    def get_update_page(self):
        """ Get the content of update novel chapter and store the chapter use a dict
        :returns: a dict of the newest page
        page = {'title': title, 'content': content}

        """
        try:
            newest_url = self.get_update_url()
            newest_page = self.open_url(newest_url)
            soup = BeautifulSoup(newest_page, 'lxml')
            title = soup.h1.string
            content_tag = soup.find('div', id="BookText")
            content = ''
            for text in content_tag.strings:
                content = content + text
            page = {'title': title, 'content': content}
        except Exception as err:
            raise err
        return page


    def load_page(self):
        """ Load the page and set the flag to false if not success
        :returns: TODO

        """
        while self.flag:
            if len(self.pages) < 1:
                try:
                    update_page = self.get_update_page()
                    if not update_page:
                        print "Fail to get the newest chapter."
                        self.flag = False
                    self.pages.append(update_page)
                except Exception as err:
                    print "Cannot connect to the webpage."
                    self.flag = False
                    raise err
        return


    def show_page(self, page):
        """ Print the page to the screen

        :page: current loaded page
        :returns: TODO

        """
        print page['title']
        print page['content']
        print '\n'
        user_input = raw_input("Type 'quit' to quit!")
        if user_input == 'quit':
            self.flag = False
        print '\n'


    def email_page(self, page):
        """ Get the page and send to the email address
        :page: the page to be emailed
        :returns: TODO

        """
        print "Sending the email..."
        msg = MIMEText(page['title'] + '\n' + page['content'], 'plain', 'utf-8')
        msg['Subject'] = 'Novel update'
        msg['From'] = 'huangww87@gmail.com'
        msg['To'] = 'huangww87@gmail.com'

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        print "Please input you password:"
        password = raw_input()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print "Email sent out."
        user_input = raw_input("Type 'quit' to quit: ")
        if user_input == 'quit':
            self.flag = False


    def start(self):
        """ Start to read the novel
        :returns: TODO

        """
        print "Loading..."

        thread.start_new_thread(self.load_page, ())
        while self.flag:
            if self.page_number <= len(self.pages):
                page = self.pages[self.page_number-1]
                self.email_page(page)
                # self.show_page(page)
                self.page_number += 1


def main():
    """ Define the interface for the program
    :returns: TODO

    """
    # Interface the the program
    print u"""
    ----------------------------------------------
        Program: Novel Spider
        Version: 1.0
        Author: Wallen
        Date: 2017-03-31
        Language: Python 2.7
        Features: Get the newest novel chapter
    ----------------------------------------------
    """

    spider = NovelSpider()
    spider.start()


if __name__ == "__main__":
    main()
