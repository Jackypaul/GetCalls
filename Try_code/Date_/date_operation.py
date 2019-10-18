#!/usr/bin/python2
# Feel free to modify the code
import getopt
from datetime import datetime
import retinasdk
import sys
import json
import MySQLdb
from string import maketrans

host='127.0.0.1'
user='root'
passwd='root'
db='Technofi'
fullClient = retinasdk.FullClient("1e7d8460-5a86-11e8-9172-3ff24e827f76")
conn = MySQLdb.connect(host=host, user=user, passwd=passwd,
                       db=db, charset="utf8", use_unicode=True)

cY = datetime.now().year
cD = datetime.now().day
cM = datetime.now().month

def ltos(l): #list to string
    ret = ""
    for e in l:
        ret = e + ' '+ ret
    return ret

def make_query(conn, tables, column, var_where=None):
    string = "Select "
    for c in column:
        string += c + (',',' ')[c == column[len(column)-1]]
    string += "from " + tables
    if (var_where):
        string += " where " + var_where
    conn.query(string)
    r = conn.store_result()
    return r.fetch_row(maxrows=0,how=1)

call = make_query(conn, "Calls", ["id","Topic_description","Topic", "Header_info"])

def check_date(string):
    M = ["Nothing","January","February","March","April","May","June","July","August","September","October","November","December"]
    l = string.split(' ')

    if int(l[-1]) > cY:
        return 1
    if int(l[-1]) == cY and M.index(l[-2]) > cM:
        return 1
    if int(l[-1]) == cY and M.index(l[-2]) == cM and int(l[-3]) > cD:
        return 1
    return 0

def get_info(info):
    lw =[]
    for h in H_info:
        lw.append(h)
    lw.sort
    for h in lw:
        if (h.startswith("Deadline")):
            if (check_date(H_info[h]) < 1):
                return (0)
            else:
                print h, " ", H_info[h]
                return (1)

i = 0
for one in call:
    topic = one['Topic'].encode('utf-8')
    topic_d = one['Topic_description'].encode('utf-8')
    H_info = json.loads(one['Header_info'])

    i += get_info(H_info)
print i

# Stages
# Topic
# Budget (EUR) - Year: 2017 
# Budget (EUR) - Year: 2016 
# Opening date
# Deadline

# Stages
# Topic
# Budget (EUR) - Year: 2017 
# Opening date
# Stages
# Deadline
