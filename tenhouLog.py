#!/usr/bin/env python
#coding=utf-8

import re

class game(object):
    """docstring for game"""
    def __init__(self, jsonObj):
        super(game, self).__init__()
        self.jsonObj = jsonObj

        self.players = [
            player(name  = self.jsonObj["name"][i],
                   sex   = self.jsonObj["sx"][i],
                   dan   = self.jsonObj["dan"][i],
                   rate  = self.jsonObj["rate"][i],
                   score = self.jsonObj["sc"][i * 2],
                   point = self.jsonObj["sc"][i * 2 + 1],
                   index = i) 
            for i in range(len(self.jsonObj["name"]))
        ]

        #set player rank
        orders = [
            (self.players[i].score + i * 0.1, self.players[i])
             for i in range(len(self.players))
        ]
        orders.sort(reverse = True)
        for i in range(len(self.players)):
            orders[i][1].rank = i + 1

        self.logs = [
            log(logObj = logObj)
            for logObj in self.jsonObj["log"]
        ]

        for lg in self.logs:
            for p in range(len(self.players)):
                if lg.isRichi(p):
                    lg._endScore[p] -= 1000

    def __str__(self):
        return ("<game %s>" % self.ref).encode("utf-8")

    def getPlayerIndex_ByName(self, playerName):
        for pl in self.players:
            if pl.name == playerName:
                return pl.index
        return -1

    def endScore(self, playerIndex):
        return [log.endScore[playerIndex] for log in self.logs]

    @property
    def ref(self):
        return self.jsonObj["ref"]

    @property
    def names(self):
        return self.jsonObj["name"]

    @property
    def date(self):
        return self.jsonObj["date"]

    @property
    def playerSum(self):
        return self.jsonObj["playerSum"]

    @property
    def ruleCode(self):
        return self.jsonObj["ruleCode"]

    @property
    def ruleStr(self):
        return self.jsonObj["ruleStr"]
    
class player(object):
    """docstring for player"""
    SexStringDict = {u"M" : u"男", u"F" : u"女"}
    def __init__(self, name, sex, dan, rate, score, point, index):
        super(player, self).__init__()
        self.name  = name
        self.sex   = sex
        self.dan   = dan
        self.rate  = rate
        self.score = score
        self.point = point
        self.rank  = -1
        self.index = index

    def __str__(self):
        return ("<player %s>" % self.name).encode("utf-8")

class log(object):
    """docstring for log"""
    def __init__(self, logObj):
        super(log, self).__init__()
        self.logObj = logObj
        #remove emptys
        while not self.logObj[-1]:
            self.logObj.pop()

        self._playerSum = len(self.logObj[1])

        self._winnerIndex = []
        self._loserIndex = []
        if not self.isDraw:
            for row in self.changeScore:
                for i in range(self.playerSum):
                    if row[i] > 0:
                        self._winnerIndex.append(i)
                    elif row[i] < 0:
                        self._loserIndex.append(i)

        self._endScore = list()
        for i in range(self.playerSum):
            temp = self.startScore[i]
            for sc in self.changeScore:
                temp += sc[i]
            self._endScore.append(temp)

        self._fan = list()
        for lst in self.yakus:
            temp = 0
            for yaku in lst:
                m = re.findall(r"\d{1,2}", yaku)
                if m:
                    temp += int(m[0])
            self._fan.append(temp)

        self._doraPtr_outer = [
            self.createMJCread(ID = ID, countDora = False)
            for ID in self.logObj[2]
        ]

        self._doraPtr_inner = [
            self.createMJCread(ID = ID, countDora = False)
            for ID in self.logObj[3]
        ]

        self._doraPtr = self._doraPtr_inner + self._doraPtr_outer

        self._dora       = list()
        self._dora_outer = list()
        self._dora_inner = list()
        self._dora_akai  = list()
        if not self.isDraw:
            for lst in self.yakus:
                temp1 = 0
                temp2 = 0
                temp3 = 0
                for yaku in lst:
                    if yaku.startswith(u"\u30c9\u30e9"):         #dora_outer
                        temp1 += int(re.findall(r"\d+", yaku)[0])
                    elif yaku.startswith(u"\u88cf\u30c9\u30e9"): #dora_inner
                        temp2 += int(re.findall(r"\d+", yaku)[0])
                    elif yaku.startswith(u"\u8d64\u30c9\u30e9"): #dora_akai
                        temp1 += int(re.findall(r"\d+", yaku)[0])
                        temp3 += int(re.findall(r"\d+", yaku)[0])
                self._dora.append(temp1 + temp2)
                self._dora_outer.append(temp1)
                self._dora_inner.append(temp2)
                self._dora_akai.append(temp3)

        if self.isSomeoneZimo():
            self._loserIndex=[] * len(self.endScore)

    def createMJCread(self, ID, zmCardID = None, countDora = True):
        akai = ID > 50
        zmgr = ID == 60
        if zmgr and zmCardID:
            ID = zmCardID
        if akai:
            ID = (ID % 10) * 10 + 5
        card = MJCard(ID = ID, akai = akai, zmgr = zmgr)
        if countDora:
            for ptr in self._doraPtr_inner:
                if ptr.PointTo(card):
                    card.dora_inner += 1
            for ptr in self._doraPtr_outer:
                if ptr.PointTo(card):
                    card.dora_outer += 1
        return card

    def isSomeoneZimo(self):
        if self.isDraw:
            return False
        elif len(self.changeScore) != 1:
            return False
        else:
            pls, mus = 0, 0
            for sc in self.changeScore[0]:
                if sc > 0:
                    pls += 1
                elif sc < 0:
                    mus += 1
            return pls == 1 and mus > 1 

    def isHost(self, playerIndex):
        return (self.gameWindIndex - 1) % 4 == playerIndex

    def isFulu(self, playerIndex):
        for cID in self.logObj[5 + playerIndex * 3]:
            if type(cID) == unicode:
                if u"c" in cID:
                    return True
                elif u"p" in cID:
                    return True
                elif u"k" in cID:
                    return True
        return False

    def isRichi(self, playerIndex):
        Rtime = 0
        for cID in self.logObj[6 + playerIndex * 3]:
            Rtime += 1
            if type(cID) == unicode:
                if u"r" in cID:
                    return True
        return False

    def isDama(self, playerIndex):
        if not self.isWin(playerIndex):
            return False
        if self.isFulu(playerIndex):
            return False
        if self.isRichi(playerIndex):
            return False
        return True

    def isWin(self, playerIndex):
        if self.isDraw:
            return False
        else:
            for sc in self.changeScore:
                if sc[playerIndex] < 0:
                    return False
                if sc[playerIndex] > 0:
                    return True
            return False

    def isChong(self, playerIndex):
        if self.isDraw:
            return False
        elif self.isSomeoneZimo():
            return False
        else:
            for sc in self.changeScore:
                if sc[playerIndex] > 0:
                    return False
                if sc[playerIndex] < 0:
                    return True
            return False

    def isZimo(self, playerIndex):
        if not self.isSomeoneZimo():
            return False
        elif len(self.changeScore) != 1:
            return False
        else:
            return self.changeScore[0][playerIndex] > 0

    def isRong(self, playerIndex):
        if not self.isWin(playerIndex):
            return False
        else:
            return not self.isSomeoneZimo()

    def isDoubleChong(self, playerIndex):
        if self.isChong(playerIndex):
            return len(self.changeScore)
        else:
            return 0

    def isOtherZimo(self, playerIndex):
        if not self.isSomeoneZimo():
            return False
        else:
            return not self.isZimo(playerIndex)

    def endRound(self, playerIndex):
        return len( self.logObj[6 + playerIndex * 3] )

    def isYifa(self,playerIndex):
        if self.isDraw:
            return False
        for i in range(len(self.changeScore)):
            if self.changeScore[i][playerIndex] > 0:
                for yaku in self.yakus[i]:
                    if u"\u4e00\u767a" in yaku:
                        return True
        return False

    @property
    def doraPtr(self):
        return self._doraPtr

    @property
    def doraPtr_outer(self):
        return self._doraPtr_outer

    @property
    def doraPtr_inner(self):
        return self._doraPtr_inner  

    @property
    def dora(self):
        return self._dora
    
    @property
    def dora_outer(self):
        return self._dora_outer

    @property
    def dora_inner(self):
        return self._dora_inner

    @property
    def dora_akai(self):
        return self._dora_akai      

    @property
    def playerSum(self):
        return self._playerSum
    
    @property
    def name(self):
        return log.gameIndexDes(self.logObj[0])

    @property
    def isDraw(self):
        return self.result != u'和了'
    
    @property
    def _resultObj(self):
        return self.logObj[4 + 3 * self._playerSum]

    @property
    def result(self):
        return self._resultObj[0]

    @property
    def changeScoreDes(self):
        if self.isDraw:
            return [self.result]
        else:
            return [lst[3] for lst in self._resultObj[2::2]]
    
    @property
    def fan(self):
        return self._fan   

    @property
    def yakus(self):
        if self.isDraw:
            return []
        else:
            return [lst[4:] for lst in self._resultObj[2::2]]

    @property
    def yakuNames(self):
        return [[n[:-4] for n in yakus if not u'\u30c9\u30e9' in n]
                for yakus in self.yakus]
    
    @property
    def gameWindIndex(self):
        return self.logObj[0][0]

    @property
    def gameRoundIndex(self):
        return self.logObj[0][1]

    @property
    def winnerIndex(self):
        return self._winnerIndex

    @property
    def loserIndex(self):
        return self._loserIndex
    
    @property
    def startScore(self):
        return self.logObj[1]
        
    @property
    def changeScore(self):
        if self.isDraw:
            if len(self._resultObj) > 1:
                return [self._resultObj[1]]
            else:
                return [[0] * self.playerSum]
        else:
            return self._resultObj[1::2]

    @property
    def endScore(self):
        return self._endScore  

    @staticmethod
    def gameIndexDes(indexTuple):
        changfeng = MJCard.dxnb[indexTuple[0] / 4 + 1]
        changshu  = MJCard.chnum(indexTuple[0] % 4 + 1)
        changju   = indexTuple[1]
        return u"%s%s局%s本场" % (changfeng, changshu, changju)       
    
class MJCard(object):
    """docstring for MJCard"""
    PostfixNames = [
        u"", u"萬", u"筒", u"索", u""
    ]
    WordPerfixNames = [
        u"", u"東", u"南", u"西", u"北", u"白", u"發", u"中"
    ]
    dxnb = [
        u"", u"東", u"南", u"西", u"北"
    ]
    numb = [
        u"零", u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"
    ]
    numx = [
        u"", u"十", u"百", u"千", u"万", u"十万", u"百万", u"千万", u"亿"
    ]

    def __init__(self, ID, akai = False, zmgr = False):
        super(MJCard, self).__init__()
        self.ID = int(ID)
        self.akai = akai
        self.zmgr = zmgr
        self.dora_outer = 0
        self.dora_inner = 0

        text = u"赤" if self.akai else u""
        if self.ID > 40:
            text += MJCard.WordPerfixNames[self.ID % 10]
        else:
            text += MJCard.chnum(self.ID % 10) + MJCard.PostfixNames[self.ID / 10]
        self._name = text

    def __str__(self):
        return self._name.encode("utf-8")
    
    def __lt__(self, target):
        return self.ID < target.ID

    def PointTo(self, target):
        if not target:
            return False
        if self.ID / 10 != target.ID / 10:
            return False
        else:
            distance = target.ID - self.ID
            return distance == 1 or distance == -8

    @property
    def name(self):
        return self._name

    @property
    def dora(self):
        return self.dora_inner + self.dora_outer

    @staticmethod
    def chnum(num):
        num = abs(int(num))
        if num == 0:
            return MJCard.numb[num]
        s = u""
        upper = False
        for lvl in range(10, -1, -1):
            x = num / (10 ** lvl)
            if x:
                upper = True
                num -= x * (10 ** lvl)
                s += MJCard.numb[x] + MJCard.numx[lvl]
            elif upper:
                upper = False
                s += MJCard.numb[x]
        return s
        

if __name__ == "__main__":        
    import sys
    import tenhouDB

    #jsons = tenhouDB.get_Jsons(tenhouDB.get_refs(name = "Rnd495", limit = 10))
    jsons = tenhouDB.get_Jsons(["2014030901gm-0009-6140-7e12757a"])
    g = game(jsons[0])

    log = g.logs[1]
    for l in g.logs:
        if len(l.yakus)>1:
            log = l
            break

    print g
    print [pl.name for pl in g.players]

    for i in log.logObj:
        print i

    print "line :", log.logObj[5 + 3 * 3]

    for i in range(len(log.fan)):
            print "Yakus:", log.changeScoreDes[i].encode("utf-8")
            print "Dora:", log.dora[i], log.dora_outer[i], log.dora_inner[i], log.dora_akai[i]
            for yaku in log.yakus[i]:
                print yaku.encode("utf-8"), (yaku, )