#!/usr/bin/python2

import getopt, retinasdk,sys,json,MySQLdb,os
from string import maketrans
from datetime import datetime
from multiprocessing import Pool
from functools import partial

llink = ["http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lc-sc3-res-8-2019.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lc-sc3-res-7-2019.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/ce-nmbp-25-2019.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lc-eeb-05-2019-20.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lce-prize-renewablehospital-01-2016.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lc-sc3-res-5-2018.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lc-sc3-res-2-2018.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lc-sc3-ee-6-2018-2019-2020.html",
"http://ec.europa.eu/research/participants/portal/desktop/en/opportunities/h2020/topics/lc-sc3-res-12-2018.html"]

host="127.0.0.1"
user="root"
passwd="root"
db="Technofi"
fullClient = retinasdk.FullClient("1e7d8460-5a86-11e8-9172-3ff24e827f76")
conn = MySQLdb.connect(host=host, user=user, passwd=passwd,
                       db=db, charset="utf8", use_unicode=True)
cY = datetime.now().year
cD = datetime.now().day
cM = datetime.now().month
nbr_calls_display = 10

client_text_all = " "

f = open('./text.txt', 'r')
text_client = f.read()
f.close()

tc = text_client.encode("utf8")

class Stacker:
    def __init__(self,ide,url,cosine):
        self.ide = ide
        self.url = url
        self.cosine = cosine

def make_query(conn, tables, column, var_where=None):
    string = "Select "
    for c in column:
        string += c + (',',' ')[c == column[len(column)-1]]
    string += "from " + tables
    if (var_where):
        string += " where " + var_where
    conn.query(string)
    r = conn.store_result() #use_result function ties up the ressource server
    return r.fetch_row(maxrows=0,how=1)

def build_cmpC(topic_d, c_text):
    lw =[]
    function = []
    ret = []
    for h in topic_d:
        lw.append(h)
    lw.sort
    for h in lw:
        if (h.startswith("Specific Challenge") or h.startswith("Expected Impact") or h.startswith("Scope")):
            ret.append([{"text":' '.join(topic_d[h])}, {"text": c_text}])
    return ret

def ft_compare(one, c_text):
    trantab = maketrans(":([{}])\"", "        ")
    call_txt=""
    topic = one['Topic'].encode('utf-8')
    topic_d = json.loads(one['Topic_description'].encode('utf-8'))
    H = json.loads(one['Header_info'])
    if ( topic_d and valid_date(H)):
        comparaison = build_cmpC(topic_d, c_text)
        c = 0
        for r in fullClient.compareBulk(json.dumps(comparaison)):
            print float(str(r)[25:40])
            c += float(str(r)[25:40])
        return (Stacker(one["id"], one["Url"], c))
    return "blank"
