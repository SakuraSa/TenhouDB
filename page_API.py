#!/usr/bin/env python
#coding=utf-8

import web
import tenhouDB
import tenhouLog
import tenhouStatistics
import datetime
import json
import re
import hashlib

class page_API(object):
    """docstring for page_API"""
    APIs = []
    def __init__(self):
        super(page_API, self).__init__()

    @staticmethod
    def regist(cls):
        if issubclass(cls, APIbase):
            page_API.APIs.append(cls())
        return cls

    def GET(self):
        webInput = web.input()
        method = webInput.get("method", None)
        if not method:
            return "error: param method is not found."
        for api in page_API.APIs:
            if method == api.name:
                return api(webInput)
        return "error: unkown method %s" % (method, )

class APIbase(object):
    """docstring for APIbase"""
    name   = "base"
    params = []
    option = {}
    def __init__(self):
        object.__init__(self)

    def __call__(self, webInput):
        kargs = dict()
        for key in self.params:
            value = webInput.get(key, None)
            if value is None:
                return "error: param %s is not found." % (key, )
            else:
                kargs[key] = value
        for key in self.option:
            value = webInput.get(key, None)
            if value is None:
                kargs[key] = self.option[key]
            else:
                kargs[key] = value
        return self.work(**kargs)

    def work(self, **kargs):
        return "error: abstract method called."

@page_API.regist
class API_APIList(APIbase):
    """docstring for API_APIList"""
    name   = "APIList"
    params = []
    option = {}
    def __init__(self):
        APIbase.__init__(self)

    def work(self):
        return json.dumps(
            [dict(name=api.name, 
                params=api.params, 
                option=api.option) for api in page_API.APIs]
            )

@page_API.regist
class API_createLog(APIbase):
    """docstring for API_createLog"""
    name   = "createLog"
    params = ["ref"]
    option = {"getJson": False}
    def __init__(self):
        APIbase.__init__(self)
            
    def work(self, ref, getJson):
        res = tenhouDB.ref_regex.findall(ref)
        if not res:
            return "error: illigal input of ref"
        res = res[0]
        obj = None
        try:
            obj = tenhouDB.addLog(ref = res)
        except Exception, e:
            return "error: %s", (e, )
        if getJson:
            return json.dumps(obj, cls=CJsonEncoder)
        else:
            return "ok"

@page_API.regist
class API_logChart(APIbase):
    """docstring for API_logChart"""
    name   = "logChart"
    params = ["ref"]
    option = {}
    def __init__(self):
        APIbase.__init__(self)
        
    def work(self, ref):
        res = tenhouDB.ref_regex.findall(ref)
        if not res:
            return "error: illigal input of ref"
        res = res[0]
        game = None
        try:
            obj = tenhouDB.addLog(ref = res)
            game = tenhouLog.game(obj)
        except Exception, e:
            return "error: %s", (e, )
        dic = dict()
        dic["playerSum"] = len(game.players)
        dic["players"]   = [dict(name           = pl.name, 
                                 score          = pl.score, 
                                 point          = pl.point, 
                                 rank           = pl.rank, 
                                 sex            = pl.sex,
                                 dan            = pl.dan,
                                 rate           = pl.rate,
                                 index          = pl.index) for pl in game.players]
        dic["logs"]      = [dict(name           = log.name, 
                                 isDraw         = log.isDraw,
                                 isZimo         = log.isSomeoneZimo(),
                                 winnerIndex    = log.winnerIndex,
                                 loserIndex     = log.loserIndex,
                                 startScore     = log.startScore,
                                 endScore       = log.endScore,
                                 result         = log.result,
                                 changeScore    = log.changeScore,
                                 changeScoreDes = log.changeScoreDes,
                                 yakus          = log.yakus) for log in game.logs]
        dic["ref"] = game.ref
        dic["date"] = game.date
        return json.dumps(dic, cls=CJsonEncoder)

@page_API.regist
class API_statistics(APIbase):
    """docstring for API_statistics"""
    name   = "statistics"
    params = ["name"]
    option = {"limit": 50,
              "lobby": None,
              "after": None,
              "before": None,
              "rule": None}
    def __init__(self):
        APIbase.__init__(self)
        
    def work(self, name, limit, lobby, after, before, rule):
        before = datetimeParse(before)
        after = datetimeParse(after)
        limit = intParse(limit)
        params = list()
        params.append(name)
        params.append(str(limit))
        if not after is None:
            params.append(after.ctime())
        if not before is None:
            params.append(before.ctime())
        if not lobby is None:
            params.append(lobby)
        if not rule is None:
            params.append(rule)
        joinstr = name.encode("utf-8") + ", " + ", ".join(params[1:])
        hashs = hashlib.sha256(joinstr).hexdigest()
        cache = tenhouDB.get_statistics_cache(hashs = hashs)
        if cache:
            return cache
        else:
            refs = tenhouDB.get_refs(name = name,
                                     limit = limit,
                                     lobby = lobby,
                                     ruleCode = rule,
                                     after = after,
                                     before = before)
            if len(refs) < 30:
                return "error :need more than 30 logs to get statistics."
            jsons = tenhouDB.get_Jsons(refs)
            games = [tenhouLog.game(js) for js in jsons]
            ps    = tenhouStatistics.PlayerStatistic(games = games, playerName = name)
            js    = ps.json()
            tenhouDB.set_statistics_cache(name = name, hashs = hashs, json = js)
            return js

@page_API.regist
class API_hotIDs(APIbase):
    """docstring for API_hotIDs"""
    name   = "hotIDs"
    params = []
    option = {"limit": 50,
              "morethan": 30}
    def __init__(self):
        APIbase.__init__(self)
        
    def work(self, limit):
        return json.dumps(
            [dict(name = row[0], count = row[1]) 
             for row in tenhouDB.get_hotIDs(limit = limit, morethan = morethan)])


def datetimeParse(text):
    if text is None:
        return None
    try:
        return datetime.datetime.strptime(text, "%Y-%m-%d-%H:%M:%S")
    except Exception, e:
        return None

def intParse(text):
    if text is None:
        return None
    try:
        return int(text)
    except Exception, e:
        return None

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    print "API list:"
    for api in page_API.APIs:
        print "name  :", api.name
        print "params:", api.params
        print "option:", api.option
        print ""