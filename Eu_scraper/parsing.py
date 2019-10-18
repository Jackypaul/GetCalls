from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import MySQLdb
import json
import re
import collections

class Read_projects:
    
    def launchBrowser(self, s, ft_ddb):
        binary = FirefoxBinary('/usr/bin/firefox')
        browse = webdriver.Firefox(firefox_binary=binary)
        browse.get(s)
        html_source = browse.page_source
        browse.quit()
        soup = BeautifulSoup(html_source,'html.parser')
        return self.parsPage(soup, ft_ddb, s)

    def parsPage(self,soup, ft_ddb, url):
        # /C/ This can change it's the tag for all text banner wich contains topic description if this tag change in the page all code is useless.
        # So you can keep the send_to_DB() function if this append. And recode a scraper.
        div_cnt = soup.find_all('div', class_="span9")
        if (div_cnt == []):
            return ('404 error or nothing in div')
        lm = div_cnt[0].find('h3').text
        Topic = lm[8:]
        Topic_id = div_cnt[1].find_all('td')[1].text #topic id value
        Budget = self.get_correct_budget(div_cnt, Topic_id)
        Action_type = ""
        Opening_date = ""
        Deadline_model = ""
        Topic_description = {}
        Topic_condition = {}
        Content = {}
        j = 0
        tdd = div_cnt[0].find('div', id="budgetTable").find_all('tr')
        while (j < len(tdd)):
            i = 0
            while (i < len(tdd[j].find_all('td'))):
                trr = tdd[j].find_all('td')[i]
                s = self.removeNonAscii(trr.text)
                Content[self.removeNonAscii(tdd[0].find_all('th')[i].text)] = s
                if (i+1 == len(tdd[j].find_all('td'))):
                    # for understand this line, first read slowly, this just get the deadline date
                    Content['Deadline'] = tdd[1].find_all('td')[len(tdd[1].find_all('td'))-1].text.split('\t')[len(tdd[1].find_all('td')[len(tdd[1].find_all('td'))-1].text.split('\t'))-1] 
                    if (Content['Topic'][0:len(Topic_id)] == Topic_id):
                        break
                i+=1
            j+=1

        # This get approximatively informations about action type, open date and dead line. But Content wich is fill up here got all of this perfectly.
        # This loop is here for visual aspect see in database, yes it can be erase and replace by a little parsing function for Content{}
        for tdd in div_cnt[1].find_all('td'):
            s = self.removeNonAscii(tdd.text)
            print "START ::: ", s
            if (s.startswith("Types of action")):
                Action_type = (self.removeNonAscii(tdd.find_next('td').text))
            if (s.startswith("Deadline:")):
                Opening_date = (self.removeNonAscii(tdd.find_next('td').text))
            if (s.startswith("DeadlineModel:")):
                Deadline_model = (self.removeNonAscii(tdd.find_next('td').text))

        # this loop is for get Topic Description and Topic conditions
        # /C/ check the tag of tittle
        for tdd in div_cnt[2].find_all('h5'):
            s = tdd.text
            print s
            if (s.startswith("Topic Description")):
                Topic_description = self.extract_description(tdd.find_previous('div'));
            if (s.startswith("Topic conditions")):
                Topic_condition = self.extract_condition(tdd.find_previous('div').find_all('p'));
                
        self.send_to_DB(ft_ddb,Topic,Topic_id,Budget,Action_type,
                        Opening_date,Deadline_model,Topic_description,Topic_condition, Content, url)
        return (Topic + ' >>> NOW IN DATABASE')
                
    def send_to_DB(self,ft_ddb,Topic,Topic_id,Budget,Action_type,
                   Opening_date,Deadline_model,Topic_description,Topic_condition, Header_info, url):
        # /C/ The comment in execute is important, the number of %s is equal to variable sent
        ft_ddb.cursor().execute("""INSERT INTO Calls (Topic,Topic_id,Budget,Action_type,
        Opening_date,Deadline_model,Topic_description,Topic_condition,Header_info, Url) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s, %s)""",
        (Topic,
         Topic_id,
         Budget,
         Action_type,
         Opening_date,
         Deadline_model,
         json.dumps(Topic_description),
         json.dumps(Topic_condition),
         json.dumps(Header_info),
         url))
        ft_ddb.commit() # Send data to database
        
    def make_text(self, des): # This function take a dict and change it to a unique string
        ret = ''
        for d in des:
            for s in des[d]:
                ret = s.encode('utf-8') + ' ' + ret
        return (ret)
    
    def strcmp(self,s1,s2): # Yes string compare i prefer my own (work better for me)
        i=0
        s1 = ' '.join(s1.split())
        if (len(s1) != len(s2)) : return 1
        while (i < len(s1)):
            if (s1[i] != '\0' and s2[i] != '\0'):
                if (s1[i] != s2[i]):
                    return 1
            i = i + 1
            return 0

    def removeNonAscii(self,s): # The name describe well the fonction's action
        ret = "".join(i for i in s if ord(i)<128)
        ret = re.sub(r'(^[ \t^]+|[ \t^]+(?=:)+)', '', ret, flags=re.M)
        ret = re.sub(r'(^[ \n^]+|[ \n^]+(?=:)+)', '', ret, flags=re.M)
        return ''.join(ret.splitlines())

    def get_correct_budget(self,div_cnt, topic_id): # this function might be useless and The loop for Content{} scrap it better
        i = 0
        while (i < len(div_cnt[0].find('div', id="budgetTable").find_all('td'))):
            tdd = div_cnt[0].find('div', id="budgetTable").find_all('td')
            s = self.removeNonAscii(tdd[i].text)
            if (s[0:len(topic_id)] == topic_id):
                if (s[0:1].isdigit()):
                    return (s)
                else:
                    s = self.removeNonAscii(tdd[i+1].text)
                    if (s[0:1].isdigit()):
                        return (s)
                    else:
                        return (self.removeNonAscii(tdd[i+2].text))
            i+=1
        return ("null")

    # /C/ This can change if span not wrap text anymore
    def extract_description(self,t):
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

    # /C/ This can change if span not wrap text anymore
    def extract_condition(self,t):
        ret = {}
        di = {}
        link= {}
        balise_name = ''
        for i in t:
            if (i.find('span')):
                balise_name = i.find('span').text
                for a in i.find_all('a'):
                    link[a.text] = a['href']
                di['link'] = link
                di['text'] = i.text
                ret[balise_name] = di
        return (ret)
