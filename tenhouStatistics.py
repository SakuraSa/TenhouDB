#!/usr/bin/env python
#coding=utf-8

from tenhouLog import *
import json
import math
import datetime

class Statistic(object):
    """docstring for Statistic"""
    def __init__(self):
        super(Statistic, self).__init__()
        self.datas = list()

    def add(self, data):
        self.datas.append(data)

    def max(self):
        if not self.datas:
            return 0
        return max(self.datas)

    def min(self):
        if not self.datas:
            return 0
        return min(self.datas)

    def sum(self):
        if not self.datas:
            return 0
        return sum(self.datas)

    def sum_not_zero(self):
        s = 0
        for data in self.datas:
            if data != False:
                s += data
        return s

    def len(self):
        return len(self.datas)

    def len_not_zero(self):
        c = 0
        for data in self.datas:
            if data != False:
                c += 1
        return c

    def avg(self):
        if not self.datas:
            return 0
        return float(sum(self.datas)) / len(self.datas)

    def avg_not_zero(self):
        s, c = 0, 0
        for data in self.datas:
            if data != False:
                s += data
                c += 1
        if c:
            return float(s) / c
        else:
            return 0

    def avg_bool(self):
        if not self.datas:
            return 0
        s = 0
        for data in self.datas:
            if data != False:
                s += bool(data)
        return float(s) / len(self.datas)

    def group(self):
        temp = dict()
        for d in self.datas:
            temp[d] = temp.get(d, 0) + 1
        return temp

    def groupPercent(self):
        temp = self.group()
        for key in temp:
            temp[key] /= float(len(self.datas))
        return temp

class PlayerStatistic(object):
    """docstring for Statistic"""
    def __init__(self, games, playerName):
        super(PlayerStatistic, self).__init__()
        self.games = games
        self.playerName = playerName

        self.rank                    = Statistic()          #平均顺位,1234位率
        self.east_rank               = Statistic()          #东起_平均顺位,1234位率
        self.south_rank              = Statistic()          #南起_平均顺位,1234位率
        self.west_rank               = Statistic()          #西起_平均顺位,1234位率
        self.north_rank              = Statistic()          #北起_平均顺位,1234位率
        self.endScore                = Statistic()          #场终得点
        self.minusScore              = Statistic()          #飞了
        self.minusOther              = Statistic()          #飞人
        self.minusOther_sum          = Statistic()          #飞人_人数
        self.dora                    = Statistic()          #Dora
        self.dora_outer              = Statistic()          #表Dora
        self.dora_inner              = Statistic()          #里Dora
        self.dora_akai               = Statistic()          #赤Dora
        self.winGame                 = Statistic()          #和了
        self.winGame_host            = Statistic()          #和了_自亲
        self.winGame_zimo            = Statistic()          #和了_自摸
        self.winGame_rong            = Statistic()          #和了_荣
        self.winGame_fulu            = Statistic()          #和了_副露
        self.winGame_richi           = Statistic()          #和了_立直
        self.winGame_score           = Statistic()          #和了_点数
        self.winGame_round           = Statistic()          #和了_巡数
        self.winGame_dama            = Statistic()          #和了_默听
        self.fulu                    = Statistic()          #副露
        self.fulu_winGame            = Statistic()          #副露_和了
        self.fulu_zimo               = Statistic()          #副露_自摸
        self.fulu_rong               = Statistic()          #副露_荣
        self.fulu_chong              = Statistic()          #副露_铳
        self.fulu_score              = Statistic()          #副露_点数
        self.chong                   = Statistic()          #放铳
        self.chong_fulu              = Statistic()          #放铳_副露
        self.chong_richi             = Statistic()          #放铳_立直
        self.chong_host              = Statistic()          #放铳_自亲
        self.chong_score             = Statistic()          #放铳_点数
        self.dehost                  = Statistic()          #炸庄
        self.dehost_score            = Statistic()          #炸庄_点数
        self.otherZimo               = Statistic()          #被自摸
        self.otherZimo_score         = Statistic()          #被自摸_点数
        self.richi                   = Statistic()          #立直
        self.richi_score             = Statistic()          #立直_点数
        self.richi_winGame           = Statistic()          #立直_和了
        self.richi_zimo              = Statistic()          #立直_自摸
        self.richi_rong              = Statistic()          #立直_荣
        self.richi_yifa              = Statistic()          #立直_一发
        self.richi_chong             = Statistic()          #立直_放铳
        self.richi_otherZimo         = Statistic()          #立直_被自摸
        self.richi_draw              = Statistic()          #立直_流局
        self.richi_inner_dora        = Statistic()          #立直_里Dora

        self.yakus = dict()

        for game in self.games:
            playerIndex = game.getPlayerIndex_ByName(self.playerName)
            if playerIndex == -1:
                continue

            #with game
            self.rank.add(game.players[playerIndex].rank)
            if playerIndex == 0:
                self.east_rank.add(game.players[playerIndex].rank)
            elif playerIndex == 1:
                self.south_rank.add(game.players[playerIndex].rank)
            elif playerIndex == 2:
                self.west_rank.add(game.players[playerIndex].rank)
            elif playerIndex == 3:
                self.north_rank.add(game.players[playerIndex].rank)
            self.endScore.add(game.players[playerIndex].score)
            self.minusScore.add(game.players[playerIndex].score < 0)

            if playerIndex in game.logs[-1].winnerIndex:
                minusOther_sum = sum([pl.score < 0 for pl in game.players if pl.index != playerIndex])
            else:
                minusOther_sum = 0
            self.minusOther.add(minusOther_sum > 0)
            self.minusOther_sum.add(minusOther_sum)

            #with log
            for log in game.logs:
                isDraw        = log.isDraw
                isWin         = log.isWin(playerIndex)
                isYifa        = log.isYifa(playerIndex)
                isZimo        = log.isZimo(playerIndex)
                isRong        = log.isRong(playerIndex)
                isChong       = log.isChong(playerIndex)
                isFulu        = log.isFulu(playerIndex)
                isRichi       = log.isRichi(playerIndex)
                isHost        = log.isHost(playerIndex)
                isOtherZimo   = log.isOtherZimo(playerIndex)
                isDama        = log.isDama(playerIndex)
                endRound      = log.endRound(playerIndex)
                score         = log.endScore[playerIndex]
                scoreChange   = sum([sc[playerIndex] for sc in log.changeScore])
                index = 0
                for sc in log.changeScore:
                    if sc[playerIndex] > 0:
                        index = 0

                if isWin:
                    self.dora.add(log.dora[index])
                    self.dora_inner.add(log.dora_inner[index])
                    self.dora_outer.add(log.dora_outer[index])
                    self.dora_akai.add(log.dora_akai[index])
                self.winGame.add(isWin)
                if isWin:
                    self.winGame_host.add(isHost and scoreChange)
                    self.winGame_zimo.add(isZimo and scoreChange)
                    self.winGame_rong.add(isRong and scoreChange)
                    self.winGame_fulu.add(isFulu and scoreChange)
                    self.winGame_richi.add(isRichi and scoreChange)
                    self.winGame_score.add(scoreChange)
                    self.winGame_round.add(endRound)
                    self.winGame_dama.add(isDama and scoreChange)
                    for i in range(len(log.changeScore)):
                        if log.changeScore[i][playerIndex] > 0:
                            for yaku in log.yakuNames[i]:
                                self.yakus[yaku] = self.yakus.get(yaku, 0) + 1

                self.fulu.add(isFulu)
                if isFulu:
                    self.fulu_zimo.add(isZimo and scoreChange)
                    self.fulu_rong.add(isRong and scoreChange)
                    self.fulu_chong.add(isChong and scoreChange)
                    self.fulu_score.add(scoreChange)
                    self.fulu_winGame.add(isWin and scoreChange)
                self.chong.add(isChong)
                if isChong:
                    self.chong_fulu.add(isFulu and scoreChange)
                    self.chong_richi.add(isRichi and scoreChange)
                    self.chong_host.add(isHost and scoreChange)
                    self.chong_score.add(scoreChange)
                self.otherZimo.add(isOtherZimo)
                if isOtherZimo:
                    self.otherZimo_score.add(scoreChange)
                    self.dehost.add(isHost)
                    if isHost:
                        self.dehost_score.add(scoreChange)
                self.richi.add(isRichi)
                if isRichi:
                    self.richi_score.add(scoreChange)
                    self.richi_winGame.add(isWin and scoreChange)
                    self.richi_zimo.add(isZimo and scoreChange)
                    self.richi_rong.add(isRong and scoreChange)
                    self.richi_yifa.add(isYifa and scoreChange)
                    self.richi_chong.add(isChong and scoreChange)
                    self.richi_otherZimo.add(isOtherZimo and scoreChange)
                    self.richi_draw.add(isDraw and scoreChange)
                    if isWin:
                        self.richi_inner_dora.add(log.dora_inner[index])

    def dict(self):
        return dict(
            games                  = self.rank.len(),
            total                  = dict(avg = self.rank.avg(),
                                          groupPercent = self.rank.groupPercent()),
            east                   = dict(avg = self.east_rank.avg(),
                                          groupPercent = self.east_rank.groupPercent()),
            south                  = dict(avg = self.south_rank.avg(),
                                          groupPercent = self.south_rank.groupPercent()),
            west                   = dict(avg = self.west_rank.avg(),
                                          groupPercent = self.west_rank.groupPercent()),
            north                  = dict(avg = self.north_rank.avg(),
                                          groupPercent = self.north_rank.groupPercent()),
            endScore               = dict(avg = self.endScore.avg(),
                                          max = self.endScore.max(),
                                          min = self.endScore.min()),
            minusScore             = dict(avg = self.minusScore.avg(),
                                          sum = self.minusScore.sum()),
            minusOther             = dict(avg = self.minusOther.avg(),
                                          sum = self.minusOther.sum(),
                                          plr = self.minusOther_sum.sum()),
            dora                   = dict(avg = self.dora.avg(),
                                          max = self.dora.max()),
            dora_inner             = dict(avg = self.dora_inner.avg(),
                                          max = self.dora_inner.max()),
            winGame                = dict(avg = self.winGame.avg(),
                                          len = self.winGame.sum()),
            winGame_score          = dict(avg = self.winGame_score.avg(),
                                          max = self.winGame_score.max()),
            winGame_host           = dict(avg = self.winGame_host.avg_not_zero(),
                                          max = self.winGame_host.max(),
                                          per = self.winGame_host.avg_bool()),
            winGame_zimo           = dict(avg = self.winGame_zimo.avg_not_zero(),
                                          max = self.winGame_zimo.max(),
                                          per = self.winGame_zimo.avg_bool()),
            winGame_rong           = dict(avg = self.winGame_rong.avg_not_zero(),
                                          max = self.winGame_rong.max(),
                                          per = self.winGame_rong.avg_bool()),
            winGame_fulu           = dict(avg = self.winGame_fulu.avg_not_zero(),
                                          max = self.winGame_fulu.max(),
                                          per = self.winGame_fulu.avg_bool()),
            winGame_richi          = dict(avg = self.winGame_richi.avg_not_zero(),
                                          max = self.winGame_richi.max(),
                                          per = self.winGame_richi.avg_bool()),
            winGame_dama           = dict(avg = self.winGame_dama.avg_not_zero(),
                                          max = self.winGame_dama.max(),
                                          per = self.winGame_dama.avg_bool()),            
            winGame_round          = dict(avg = self.winGame_round.avg_not_zero(),
                                          min = self.winGame_round.min()),
            fulu                   = dict(avg = self.fulu.avg(),
                                          len = self.fulu.sum()),
            fulu_winGame           = dict(per = self.fulu_winGame.avg_bool()),
            fulu_score             = dict(avg = self.fulu_score.avg(),
                                          max = self.fulu_score.max(),
                                          min = self.fulu_score.min()),
            fulu_zimo              = dict(avg = self.fulu_zimo.avg_not_zero(),
                                          max = self.fulu_zimo.max(),
                                          per = self.fulu_zimo.avg_bool()),
            fulu_rong              = dict(avg = self.fulu_rong.avg_not_zero(),
                                          max = self.fulu_rong.max(),
                                          per = self.fulu_rong.avg_bool()),
            fulu_chong             = dict(avg = self.fulu_chong.avg_not_zero(),
                                          min = self.fulu_chong.min(),
                                          per = self.fulu_chong.avg_bool()),
            chong                  = dict(avg = self.chong.avg(),
                                          len = self.chong.sum()),
            chong_score            = dict(avg = self.chong_score.avg(),
                                          min = self.chong_score.min()),
            chong_host             = dict(avg = self.chong_host.avg_not_zero(),
                                          min = self.chong_host.min(),
                                          per = self.chong_host.avg_bool()),
            chong_fulu             = dict(avg = self.chong_fulu.avg_not_zero(),
                                          min = self.chong_fulu.min(),
                                          per = self.chong_fulu.avg_bool()),
            chong_richi            = dict(avg = self.chong_richi.avg_not_zero(),
                                          min = self.chong_richi.min(),
                                          per = self.chong_richi.avg_bool()),
            dehost                 = dict(avg = self.dehost.avg(),
                                          len = self.dehost.sum()),
            dehost_score           = dict(avg = self.dehost_score.avg(),
                                          min = self.dehost_score.min()),
            otherZimo              = dict(avg = self.otherZimo.avg(),
                                          len = self.otherZimo.sum()),
            otherZimo_score        = dict(avg = self.otherZimo_score.avg(),
                                          min = self.otherZimo_score.min()),
            richi                  = dict(avg = self.richi.avg(),
                                          len = self.richi.sum()),
            richi_winGame          = dict(per = self.richi_winGame.avg_bool()),
            richi_score            = dict(avg = self.richi_score.avg(),
                                          min = self.richi_score.min(),
                                          max = self.richi_score.max()),
            richi_yifa             = dict(avg = self.richi_yifa.avg_not_zero(),
                                          max = self.richi_yifa.max(),
                                          per = self.richi_yifa.avg_bool()),
            richi_rong             = dict(avg = self.richi_rong.avg_not_zero(),
                                          max = self.richi_rong.max(),
                                          per = self.richi_rong.avg_bool()),
            richi_zimo             = dict(avg = self.richi_zimo.avg_not_zero(),
                                          max = self.richi_zimo.max(),
                                          per = self.richi_zimo.avg_bool()),
            richi_chong            = dict(avg = self.richi_chong.avg_not_zero(),
                                          min = self.richi_chong.min(),
                                          per = self.richi_chong.avg_bool()),
            richi_draw             = dict(per = self.richi_draw.avg_bool()),
            richi_otherZimo        = dict(avg = self.richi_otherZimo.avg_not_zero(),
                                          min = self.richi_otherZimo.min(),
                                          per = self.richi_otherZimo.avg_bool()),
            richi_inner_dora       = dict(avg = self.richi_inner_dora.avg(),
                                          max = self.richi_inner_dora.max()),
            yakus                  = [[self.yakus[yaku], yaku] for yaku in self.yakus],
        )

    def json(self):
        return json.dumps(self.dict())

if __name__ == "__main__":
    import tenhouDB

    playerName = u"pleuvoir"
    jsons = tenhouDB.get_Jsons(tenhouDB.get_refs(
        name = playerName, 
        limit = 1000))
    games = [game(js) for js in jsons]
    ps    = PlayerStatistic(games = games, playerName = playerName)

    print "games                      :", len(games)
    print "total                      :", ps.rank.avg(), ps.rank.groupPercent()
    print "east                       :", ps.east_rank.avg(), ps.east_rank.groupPercent()
    print "south                      :", ps.south_rank.avg(), ps.south_rank.groupPercent()
    print "west                       :", ps.west_rank.avg(), ps.west_rank.groupPercent()
    print "north                      :", ps.north_rank.avg(), ps.north_rank.groupPercent()
    print "endScore                   :", "max =", ps.endScore.max(), "; min =", ps.endScore.min(), "; avg =", ps.endScore.avg()
    print "minusScore                 :", "avg =", ps.minusScore.avg(), "; sum =", ps.minusScore.sum()
    print "minusOther                 :", "avg =", ps.minusOther.avg(), "; sum =", ps.minusOther.sum(), "; player =", ps.minusOther_sum.sum()
    print "dora                       :", "avg =", ps.dora.avg(), "; max =", ps.dora.max()
    print "winGame                    :", "avg =", ps.winGame.avg(), "; len =", ps.winGame.sum()
    print "winGame_score              :", "avg =", ps.winGame_score.avg(), "; max =", ps.winGame_score.max()
    print "winGame_host               :", "per =", ps.winGame_host.avg_bool(), "; avg =", ps.winGame_host.avg_not_zero(), "; max =", ps.winGame_host.max()
    print "winGame_zimo               :", "per =", ps.winGame_zimo.avg_bool(), "; avg =", ps.winGame_zimo.avg_not_zero(), "; max =", ps.winGame_zimo.max()
    print "winGame_rong               :", "per =", ps.winGame_rong.avg_bool(), "; avg =", ps.winGame_rong.avg_not_zero(), "; max =", ps.winGame_rong.max()
    print "winGame_fulu               :", "per =", ps.winGame_fulu.avg_bool(), "; avg =", ps.winGame_fulu.avg_not_zero(), "; max =", ps.winGame_fulu.max()
    print "winGame_richi              :", "per =", ps.winGame_richi.avg_bool(), "; avg =", ps.winGame_richi.avg_not_zero(), "; max =", ps.winGame_richi.max()
    print "winGame_round              :", "avg =", ps.winGame_round.avg(), "; min =", ps.winGame_round.min()
    print "winGame_dama               :", "per =", ps.winGame_dama.avg_bool(), "; avg =", ps.winGame_dama.avg_not_zero(), "; max =", ps.winGame_dama.max()
    print "fulu                       :", "avg =", ps.fulu.avg(), "; len =", ps.fulu.sum()
    print "fulu_score                 :", "avg =", ps.fulu_score.avg(), "; max =", ps.fulu_score.max(), "; min =", ps.fulu_score.min()
    print "fulu_zimo                  :", "per =", ps.fulu_zimo.avg_bool(), "; avg =", ps.fulu_zimo.avg_not_zero(), "; max =", ps.fulu_zimo.max()
    print "fulu_rong                  :", "per =", ps.fulu_rong.avg_bool(), "; avg =", ps.fulu_rong.avg_not_zero(), "; max =", ps.fulu_rong.max()
    print "fulu_chong                 :", "per =", ps.fulu_chong.avg_bool(), "; avg =", ps.fulu_chong.avg_not_zero(), "; max =", ps.fulu_chong.min()
    print "chong                      :", "avg =", ps.chong.avg(), "; len =", ps.chong.sum()
    print "chong_score                :", "avg =", ps.chong_score.avg(), "; max =", ps.chong_score.min()
    print "chong_host                 :", "per =", ps.chong_host.avg_bool(), "; avg =", ps.chong_host.avg_not_zero(), "; max =", ps.chong_host.min()
    print "chong_fulu                 :", "per =", ps.chong_fulu.avg_bool(), "; avg =", ps.chong_fulu.avg_not_zero(), "; max =", ps.chong_fulu.min()
    print "chong_richi                :", "per =", ps.chong_richi.avg_bool(), "; avg =", ps.chong_richi.avg_not_zero(), "; max =", ps.chong_richi.min()
    print "dehost                     :", "avg =", ps.dehost.avg(), "; len =", ps.dehost.sum()
    print "dehost_score               :", "avg =", ps.dehost_score.avg(), "; max =", ps.dehost_score.min()
    print "otherZimo                  :", "avg =", ps.otherZimo.avg(), "; len =", ps.otherZimo.sum()
    print "otherZimo_score            :", "avg =", ps.otherZimo_score.avg(), "; max =", ps.otherZimo_score.min()
    print "richi                      :", "avg =", ps.richi.avg(), "; len =", ps.richi.sum()
    print "richi_score                :", "avg =", ps.richi_score.avg(), "; max =", ps.richi_score.min()
    print "richi_yifa                 :", "per =", ps.richi_yifa.avg_bool(), "; avg =", ps.richi_yifa.avg_not_zero(), "; max =", ps.richi_yifa.max()
    print "richi_rong                 :", "per =", ps.richi_rong.avg_bool(), "; avg =", ps.richi_rong.avg_not_zero(), "; max =", ps.richi_rong.max()
    print "richi_zimo                 :", "per =", ps.richi_zimo.avg_bool(), "; avg =", ps.richi_zimo.avg_not_zero(), "; max =", ps.richi_zimo.max()
    print "richi_chong                :", "per =", ps.richi_chong.avg_bool(), "; avg =", ps.richi_chong.avg_not_zero(), "; max =", ps.richi_chong.min()
    print "richi_draw                 :", "per =", ps.richi_draw.avg_bool(), "; avg =", ps.richi_draw.avg_not_zero(), "; max =", ps.richi_draw.max()
    print "richi_otherZimo            :", "per =", ps.richi_otherZimo.avg_bool(), "; avg =", ps.richi_otherZimo.avg_not_zero(), "; max =", ps.richi_otherZimo.min()
    print "richi_inner_dora           :", "avg =", ps.richi_inner_dora.avg()
    print ""
    print "Yakus:"
    order = [(ps.yakus[yaku], yaku) for yaku in ps.yakus]
    order.sort(reverse=True)
    s = ps.winGame.sum()
    for pair in order:
        print "%4d" % pair[0], "%6s" % ("%.2f" % (pair[0] * 100.0 / s)) + "%", ("%10s" % pair[1]).encode('utf-8')