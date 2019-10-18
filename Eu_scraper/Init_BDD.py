#!/usr/bin/env python
# -*- coding: utf-8 -*-from selenium import webdriver

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from parsing import Read_projects
import MySQLdb
import time

class Core_Gest:
    def __init__(self):
        self.html_source = 0
        self.soup = 0
        self.comments = 0
        self.link = 'https://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/search/search_topics.html#c,topics=callStatus/t/Closed/1/1/0/default-group'
        self.host = '127.0.0.1'
        self.db = 'Technofi'
        self.user = 'root'
        self.passwd = 'root'
        
    def Init_Data_base(self):
        pars = Read_projects()
        self.StartBrowser()
        self.wiew_all_page(pars.launchBrowser)

    def StartBrowser(self): # Launch first page where all calls appear stack them in
        
        self.binary = FirefoxBinary('/usr/bin/firefox')
        self.browser = webdriver.Firefox(firefox_binary=self.binary)
        self.browser.get(self.link)
        time.sleep(8) # Yes sleep, sometime europa.eu take a loooong time (6 sec) to get and print all calls
        self.html_source = self.browser.page_source  
        self.soup = BeautifulSoup(self.html_source,'html.parser')
        
        # /C/           id result-counteur may change
        self.comments = self.soup.findAll('div',{'id':'results-counter'}) # Return the number of calls on the page
        ok = self.extract_text(self.comments)
        print ok
        if (str(ok).startswith("[0]") == True): # Check the number of calls received, re-call fonction if none.
            self.browser.quit()
            self.StartBrowser()
        self.browser.quit()

    def extract_text(self, html_balise): # return text from html balise
        
        t = BeautifulSoup(str(html_balise), "html.parser")
        return t.get_text()
            
    def create_link_from_href(self, herf): # We need to add root url and format url on herf balise wich are formatted like this : "/something/something/call.html"        
        # /C/           Can change if url for calls change
        return("http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/" +
               (str(herf))[6:])
        

    def wiew_all_page(self, function):    # Argument must be a function. it will be send to it all the Calls link
        comments = self.soup.findAll('ul',{'id':'topics'})
        
        # /C/           can change if tag a no longer contains calls
        comment = (BeautifulSoup(str(comments), "html.parser")).find_all("a") # get all tag a
        conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd,
                               db=self.db, charset="utf8", use_unicode=True)

        for x in comment:
            ok = BeautifulSoup(str(x), "html.parser")
            

            if (ok.a['href'].startswith('http')):
                print function(ok.a['href'], conn)
            else:
                # /C/      change if link are fully understandable ex: "http://europas.eu/en/something" but not "/en/something"
                print function(self.create_link_from_href(ok.a['href']), conn) # So here call Init() function in class Read_projects
            
        conn.close()
