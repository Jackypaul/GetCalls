#!/usr/bin/python2
# Feel free to modify the code

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import MySQLdb
from parsing import Compare_project
import retinasdk
import sys
import json

# Just in case link is not clean for selenium or whatever
def conform_link(link):
    link =str(link)
    ret =''
    linkp = link.split('/')
    for part in linkp:
        part =str(part)
        if (part.startswith('www.', 0, 5)):
            return (part)
        else:
            for l in part:
                if (l == '.'):
                    if (part.startswith('www.', 0, 5)):
                        return (part)
                    else:
                        return ("www."+part)
    return (ret)

# Clean url string
def epur_links(links,link):
    to_scrap = []
    link2 = link[0:4] + 's' + link[4:]
    for l in links:
        if (l != None):
            if (l.startswith(link) or l.startswith(link2) or l.startswith("/en") or
                l.startswith("http://" + link[11:]) or l.startswith("https://" + link[11:])):
                if (len(l) > 13):
                    to_scrap.append(l)

    return (to_scrap)

# All is in the name
def get_all_link(soup):
    links =[]
    for l in soup.find_all('a'):
        links.append(l.get('href'))
    return (links)

# to scrap is all the links get on the page
def create_list_page(to_scrap,link):
    # So we need to epur other site link from site we need
    pars = Compare_project()
    list_page = []
    for l in to_scrap[0:10]:
        url = l
        if (l.startswith("/en")):
            print "link : ", link, "url : ", url
            s = pars.Init(link+url, link)
            list_page.append(s.encode('utf-8'))
        else:
            print "link : ", link, "url : ", url
            s = pars.Init(url, link)
            list_page.append(s.encode('utf-8'))
    return list_page

def ltos(l): #list to string
    ret = ""
    for e in l:
        ret = e + ' '+ ret
    return ret

def init(link,conn):

    if (link[-3:] != '/en'):
        if (link[-1:] == '/'):
            link = link + 'en'
        else:
            link = link + '/en'
    
    # Start Browser
    print link
    binary = FirefoxBinary('/usr/bin/firefox')
    browser = webdriver.Firefox(firefox_binary=binary)
    browser.get(link)
    html_source = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html_source,'html.parser')
    

    link = "http://" + conform_link(link)
    link2 = link[0:4] + 's' + link[4:]
    
    links = get_all_link(soup)
    to_scrap = epur_links(links,link)
    epur_link = conform_link(link)
    list_page = create_list_page(to_scrap,link)
    conn.cursor().execute("""INSERT INTO Extern_site (Name,Site,Word) VALUES (%s,%s,%s)""", (epur_link,link,ltos(list_page)))
    conn.commit()
    return(list_page)
