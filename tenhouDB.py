#!/usr/bin/env python
#coding=utf-8

import time
import datetime
import threading
import sqlite3
import requests
import json
import re
import os

database = sqlite3.connect("tenhou.db", check_same_thread = False)
cursor = database.cursor()
mutex = threading.Lock()
workingThread = None

def databaseOperation(func):
    def bar(*arg, **karg):
        global workingThread,mutex
        currentThread = threading.currentThread()
        otherThread = not currentThread is workingThread
        if otherThread:
            mutex.acquire(1)
            workingThread = currentThread
        ret = None
        try:
            ret = func(*arg, **karg)
        except Exception, e:
            if otherThread:
                mutex.release()
            raise e
        if otherThread:
            mutex.release()
        return ret
    return bar


ref_regex = re.compile(r"(\d{10}gm-\w{4}-\d{4,5}-\w{8})")

#init database


with open("init.sql", "r") as sqlFile:
    init_Sql = sqlFile.read().split(";")
for cmd in init_Sql:
    cursor.execute(cmd.strip())
database.commit()

ruleDic = {
    u"0007": u"般东",
    u"000f": u"般南",
    u"0003": u"般东喰",
    u"0001": u"般南喰",
    u"0007": u"般东喰赤",
    u"0009": u"般南喰赤",
    u"0041": u"般东喰赤速",
    u"0049": u"般南喰赤速",
    u"00c1": u"上东喰赤速",
    u"0089": u"上南喰赤",
    u"0061": u"特东喰赤速",
    u"0029": u"特南喰赤",
    u"00e1": u"凤东喰赤速",
    u"00a9": u"凤南喰赤",
}
errorCode = u"未知模式"
def get_info_from_ref(ref):
    date = datetime.datetime.strptime(ref[0:10], "%Y%m%d%H")
    ruleCode = ref[13:17]
    ruleStr = ruleDic.get(ruleCode, errorCode)
    lobby = ref[18:22]
    return dict(date     = date, 
                ruleCode = ruleCode, 
                ruleStr  = ruleStr, 
                lobby    = lobby)

banRuleCodes = [u"0841"]

@databaseOperation
def downloadLog(url, baseUrl = None):
    ref = ref_regex.findall(url)
    if not ref:
        raise Exception("Unexpected URL: %s" % url)
    if not baseUrl:
        reqUrl = r"http://tenhou.net/5/mjlog2json.cgi?" + ref[0]
    else:
        reqUrl = baseUrl + ref[0]
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Pragma": "no-cache", 
        "Cache-Control": "no-cache", 
        "If-Modified-Since": "Thu, 01 Jun 1970 00:00:00 GMT", 
        "Host": "tenhou.net", 
        "Referer": reqUrl, 
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36", 
    }
    req = requests.get(reqUrl, headers = headers)
    if req.status_code != 200:
        raise Exception("Can not connect with %s" % reqUrl)
    if req.text.strip() == "INVALID PATH":
        raise Exception("Return Unexpected text: %s" % req.text.strip())
    try:
        obj = req.json()
    except Exception, e:
        raise Exception("unexcepted returns [%s]" % req.text)
    
    while(not obj["name"][-1]):
        obj["name"].pop()
    if len(obj["name"]) != 4:
        raise Exception("Not 4 Player Game, skipped.")
    if not "sc" in obj:
        raise Exception("Game was stopped by host, skipped.")
    if obj["ruleCode"] in banRuleCodes:
        raise Exception("Not normal game rule %s" % obj["ruleCode"])
    return obj, req.text

@databaseOperation
def addLog(ref, baseUrl = None, noCommit = False):
    temp = cursor.execute(r'select ref from logs where ref = ?',(ref,)).fetchall()
    if not temp:
        obj, text = downloadLog(ref, baseUrl)
        info = get_info_from_ref(ref)
        cursor.execute(r"insert into logs (ref, json, gameat, rulecode, lobby, createat) values (?, ?, ?, ?, ?, ?)", 
                       (obj["ref"], text, info["date"], info["ruleCode"], info["lobby"], datetime.datetime.now()))
        for name in obj["name"]:
            cursor.execute(r"insert into logs_name (ref, name) values (?, ?)", 
                           (obj["ref"], name))
            cursor.execute(r"update statistics_cache set updated = updated - 1 where (name = ? or global) and updated > 1", (name, ))
            cursor.execute(r"delete from statistics_cache where (name = ? or global) and updated = 1" , (name, ))
        if not noCommit:
            database.commit()
        return get_Json(obj["ref"])
    else:
        return get_Json(temp[0][0])

def addLogs(refs, baseUrl = None):
    print "Adding %d logs..." % len(refs)
    start = time.time()
    counter = 0
    for ref in refs:
        counter += 1
        addLog(ref, baseUrl, noCommit = True)
        print "%4d/%4d %s compelet %fs cost." % (counter, len(refs), ref, time.time() - start)
    database.commit()
    print "All %d logs adding compele %fs cost." % (len(refs), time.time() - start)

@databaseOperation
def get_refs(name, after = None, before = None, lobby = None, ruleCode = None, limit = 10, offset = 0):
    sqlparam = [name]
    queryParam = ["name = ?"]
    if not after is None:
        sqlparam.append(after)
        queryParam.append("gameat > ?")
    if not before is None:
        sqlparam.append(before)
        queryParam.append("gameat < ?")
    if (not lobby is None) and lobby:
        sqlparam.append(lobby)
        queryParam.append("lobby = ?")
    if not ruleCode is None:
        sqlparam.append(ruleCode)
        queryParam.append("rulecode = ?")
    sqlparam.append(limit)
    sqlparam.append(offset)
    sqlcmd   = """
    select logs.ref 
    from logs inner join logs_name 
        on logs.ref = logs_name.ref 
    where %s
    order by logs.gameat desc
    limit ? offset ?;
    """ % " and ".join(queryParam)
    resLst = list()
    for row in cursor.execute(sqlcmd, sqlparam).fetchall():
        resLst.append(row[0])
    return resLst

@databaseOperation
def get_lastRefs(limit = 10):
    resLst = list()
    resSet = set()
    for row in cursor.execute(r"Select distinct ref from logs order by createat desc limit ?", (limit, )).fetchall():
        if not row[0] in resSet:
            resLst.append(row[0])
            resSet.add(row[0])
    return resLst

@databaseOperation
def get_Json(ref):
    temp = cursor.execute(r"Select json From logs where ref = ? limit 1", (ref, )).fetchall()
    if temp:
        js = json.loads(temp[0][0])
        info = get_info_from_ref(ref)
        js["date"] = info["date"]
        js["ruleCode"] = info["ruleCode"]
        js["ruleStr"] = info["ruleStr"]
        js["playerSum"] = len(js["name"])
        js["scs"] = js["sc"][::2]
        js["scp"] = js["sc"][1::2]
        return js
    else:
        return None

def get_Jsons(refs):
    resLst = list()
    for ref in refs:
        resLst.append(get_Json(ref))
    return resLst

@databaseOperation
def get_OriText(ref):
    temp = cursor.execute(r"Select json From logs where ref = ? limit 1", (ref, )).fetchall()
    if temp:
        return temp[0][0]
    else:
        addLog(ref)
        return get_OriText(ref)

@databaseOperation
def get_statistics_cache(hashs):
    temp = cursor.execute(r"select json from statistics_cache where hash = ? limit 1", (hashs, )).fetchall()
    if temp:
        return temp[0][0]
    else:
        return None

@databaseOperation
def set_statistics_cache(name, hashs, json, updated=1):
    cursor.execute(r"insert into statistics_cache(name, hash, json, updated) values (?, ?, ?, ?)", (name, hashs, json, updated))
    database.commit()

@databaseOperation
def get_hotIDs(limit = 50, morethan = 30):
    return cursor.execute("""
        select Name,CNT from (
            select distinct logs_name.name as Name, COUNT(*) as CNT 
            from logs_name join logs 
                on logs_name.ref = logs.ref
            group by logs_name.name
            order by CNT desc
        ) where CNT >= ? and not(name='NoName')
        order by CNT desc
        limit ?""", (morethan, limit, )).fetchall()

@databaseOperation
def clear_APIcache():
    cursor.execute(r"delete from statistics_cache;")

@databaseOperation
def get_Ori_log(ref):
    temp = cursor.execute(r"Select json From logs where ref = ? limit 1", (ref, )).fetchall()
    if temp:
        return temp[0][0]
    else:
        raise Exception("log <%s> not found." % ref)

@databaseOperation
def get_all_refs():
    temp = cursor.execute(r"Select ref From logs").fetchall()
    return [i[0] for i in temp]
        
if __name__ == "__main__":
    addLog('2014050117gm-0009-6140-68483c67')