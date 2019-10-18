from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import re
import collections

link = 'https://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/eic-fti-2018-2020.html'
binary = FirefoxBinary('/usr/bin/firefox')
browser = webdriver.Firefox(firefox_binary=binary)
browser.get(link)
html_source = browser.page_source
browser.quit()
soup = BeautifulSoup(html_source,'html.parser')
div_cnt = soup.find_all('div', class_="span9")
#print type(soup)
#print type(div_cnt)
#print len(div_cnt)
##print div_cnt[0]
# h3 : Topic
# td : first topic id string "Topic identifier:" in string balise
#    : second topic id value in td only
#    : first type of action string "Types of action:" in stron balise
#    : second type of action value
#    : first Deadline  string " Deadline:  " in strong balise
#    : second topic id value just in id
#print div_cnt[1].find_all('td')

def strcmp(s1,s2):
    i=0
    s1 = ' '.join(s1.split())
    if (len(s1) != len(s2)) : return 1
    while (i < len(s1)):
        if (s1[i] != '\0' and s2[i] != '\0'):
            if (s1[i] != s2[i]):
                return 1
        i = i + 1
    return 0

def removeNonAscii(s):
    ret = "".join(i for i in s if ord(i)<128)
    ret = re.sub(r'(^[ \t^]+|[ \t^]+(?=:)+)', '', ret, flags=re.M)
    ret = re.sub(r'(^[ \n^]+|[ \n^]+(?=:)+)', '', ret, flags=re.M)
    return ''.join(ret.splitlines())

def get_correct_budget(div_cnt, topic_id):
        i = 0
        while (i < len(div_cnt[0].find('div', id="budgetTable").find_all('td'))):
            tdd = div_cnt[0].find('div', id="budgetTable").find_all('td')
            s = removeNonAscii(tdd[i].text)
            if (s[0:len(topic_id)] == topic_id):
                if (s[0:1].isdigit()):
                    return (s)
                else:
                    s = removeNonAscii(tdd[i+1].text)
                    if (s[0:1].isdigit()):
                        return (s)
                    else:
                        return (removeNonAscii(tdd[i+2].text))
            i+=1
        return ("null")

def extract_description(t):
    d = collections.defaultdict(list)
    l = []
    i = 3
    balise_name = ''
    while (i < len(t.contents)):
        if (t.contents[i].name):
            if (t.contents[i].name == "span"):
                balise_name = t.contents[i].text
            else:
                l.append((balise_name, t.contents[i].text))
        i += 1
    for k, v in l:
        d[k].append(v)
    return (d)

def extract_condition(t):
    ret = {}
    di = {}
    link= {}
    balise_name = ''
    for i in t:
        #print "I in LOOP: \n",i 
        if (i.find('span')):
            balise_name = i.find('span').text
            for a in i.find_all('a'):
                link[a.text] = a['href']
            di['link'] = link
            di['text'] = i.text
            ret[balise_name] = di
            #print "\tDI\n", di, '\n'
    return (ret)

print removeNonAscii(div_cnt[1].find('h3').text)
div_cnt[1].find_all('td')[0].text #topic id string
Topic_id = div_cnt[1].find_all('td')[1].text #topic id value
Content = {}
j = 0
tdd = div_cnt[0].find('div', id="budgetTable").find_all('tr')
while (j < len(tdd)):
    i = 0
    while (i < len(tdd[j].find_all('td'))):
        trr = tdd[j].find_all('td')[i]
        s = removeNonAscii(trr.text)
        Content[ removeNonAscii(tdd[0].find_all('th')[i].text)] = s
        if (i+1 == len(tdd[j].find_all('td'))):
            Content['Deadline'] = tdd[1].find_all('td')[len(tdd[1].find_all('td'))-1].text.split('\t')[len(tdd[1].find_all('td')[len(tdd[1].find_all('td'))-1].text.split('\t'))-1]
            print Content['Topic'][0:len(Topic_id)], " to ", Topic_id
            if (Content['Topic'][0:len(Topic_id)] == Topic_id):
                print Content
                break0
        i+=1
    j+=1
    
Topic_description = {}
Topic_condition = {}
for tdd in div_cnt[2].find_all('h5'):
    ##print tdd.text,'\n',tdd.find_previous('div').text,'\n','\n'
    s = tdd.text
    if (s.startswith("Topic Description")):
       Topic_description = extract_description(tdd.find_previous('div'));
       print type(Topic_description)
    if (s.startswith("Topic conditions")):
        Topic_condition = extract_condition(tdd.find_previous('div').find_all('p'));
        print type(Topic_condition)
