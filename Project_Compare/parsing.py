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

    # def strcmp(self,s1,s2):
    #     i=0
    #     s1 = ' '.join(s1.split())
    #     if (len(s1) != len(s2)) : return 1
    #     while (i < len(s1)):
    #         if (s1[i] != '\0' and s2[i] != '\0'):
    #             if (s1[i] != s2[i]):
    #                 return 1
    #         i = i + 1
    #         return 0

    def removeNonAscii(self,s):
        ret = "".join(i for i in s if ord(i)<128)
        ret = re.sub(r'(^[ \t^]+|[ \t^]+(?=:)+)', '', ret, flags=re.M)
        ret = re.sub(r'(^[ \n^]+|[ \n^]+(?=:)+)', '', ret, flags=re.M)
        return ''.join(ret.splitlines())

    # def get_correct_budget(self,div_cnt, topic_id):
    #     i = 0
    #     while (i < len(div_cnt[0].find('div', id="budgetTable").find_all('td'))):
    #         tdd = div_cnt[0].find('div', id="budgetTable").find_all('td')
    #         s = self.removeNonAscii(tdd[i].text)
    #         if (s[0:len(topic_id)] == topic_id):
    #             if (s[0:1].isdigit()):
    #                 return (s)
    #             else:
    #                 s = self.removeNonAscii(tdd[i+1].text)
    #                 if (s[0:1].isdigit()):
    #                     return (s)
    #                 else:
    #                     return (self.removeNonAscii(tdd[i+2].text))
    #         i+=1
    #     return ("null")

    # def extract_description(self,t):
    #     d = collections.defaultdict(list)
    #     l = []
    #     i = 3
    #     balise_name = ''
    #     while (i < len(t.contents)):
    #         if (t.contents[i].name):
    #             if (t.contents[i].name == "span"):
    #                 balise_name = t.contents[i].text
    #             else:
    #                 l.append((balise_name, t.contents[i].text))
    #         i += 1
    #     for k, v in l:
    #         d[k].append(v)
    #     return (d)

    # def extract_condition(self,t):
    #     ret = {}
    #     di = {}
    #     link= {}
    #     balise_name = ''
    #     for i in t:
    #         if (i.find('span')):
    #             balise_name = i.find('span').text
    #             for a in i.find_all('a'):
    #                 link[a.text] = a['href']
    #             di['link'] = link
    #             di['text'] = i.text
    #             ret[balise_name] = di
    #     return (ret)
