from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import re

class Compare_project:

    def Init(self, url,link):
        """ Launch browser with a url in parametter and return all page"""
        binary = FirefoxBinary('/usr/bin/firefox')
        browse = webdriver.Firefox(firefox_binary=binary)
        browse.get(url)
        html_source = browse.page_source
        browse.quit()
        soup = BeautifulSoup(html_source,'html.parser')
        return (self.parsPage(soup))

    def parsPage(self, soup):
        p =  soup.find_all('p')
        li = soup.find_all('li')
        ret = ''
        for t in p:
            ret = self.removeNonAscii(t.text) + ' ' + ret
        for t in li:
            ret = self.removeNonAscii(t.text) + ' ' + ret
        return (ret)


    def removeNonAscii(self,s):
        ret = "".join(i for i in s if ord(i)<128)
        ret = re.sub(r'(^[ \t^]+|[ \t^]+(?=:)+)', '', ret, flags=re.M)
        ret = re.sub(r'(^[ \n^]+|[ \n^]+(?=:)+)', '', ret, flags=re.M)
        return ''.join(ret.splitlines())
