#!/usr/bin/env python
#coding=utf-8


import datetime
import sqlite3
import os

def combine(DBName_from, DBName_to):
    dbf = sqlite3.connect(DBName_from)
    dbfc = dbf.cursor()
    dbt = sqlite3.connect(DBName_to)
    dbtc = dbt.cursor()

    fdbd = dbfc.execute(r"select ref, json, gameat, rulecode, lobby, createat from logs").fetchall()
    tref = set([row[0] for row in dbtc.execute(r"select ref from logs").fetchall()])
    counter = 0
    for row in fdbd:
        ref = row[0]
        if not ref in tref:
            dbtc.execute(r"insert or ignore into logs (ref, json, gameat, rulecode, lobby, createat) values (?, ?, ?, ?, ?, ?)", row)
            for row1 in dbfc.execute(r"select name from logs_name where ref = ?", (row[0], )).fetchall():
                name = row1[0]
                dbtc.execute(r"insert into logs_name (ref, name) values (?, ?)", (ref, name))
            print counter, ref
            counter += 1
    dbt.commit()
    dbf.close()
    dbt.close()
    print "ok"

if __name__ == '__main__':
    combine("tenhou_remote.db", "tenhou.db")