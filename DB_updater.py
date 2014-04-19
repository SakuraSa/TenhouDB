#!/usr/bin/env python
#coding=utf-8


import datetime
import sqlite3
import os
import shutil
import json

dbname    = "tenhou.db"
tempfile  = "temp.db"
backupDir = "DBbackup"
version   = "ver0.001"

#get database version and do backup
database  = sqlite3.connect(dbname)
cursor    = database.cursor()
if cursor.execute(r"SELECT COUNT(*) as CNT FROM sqlite_master where type='table' and name='dbupdate';").fetchall()[0][0]:
    version = cursor.execute(r"SELECT value FROM dbupdate where key='version' limit 1").fetchall()[0][0]
if not os.path.exists(backupDir):
    os.mkdir(backupDir)
backupName = datetime.datetime.now().strftime("%Y%m%d%H%M%S.bk." + version)
backupPath = os.path.join(backupDir, backupName)
shutil.copyfile(dbname, backupPath)
print "Backup DB to", backupPath, "whit %d logs" % cursor.execute(r'select COUNT(*) as CNT from logs').fetchall()[0][0]
database.close()

#database update process
if version == "ver0.001":
    """
    var0.001 => ver0.002
    """

    database = sqlite3.connect(dbname)
    cursor = database.cursor()

    #add new table for database version records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dbupdate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key char(40) NOT NULL,
            value text NOT NULL,
            attime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
        );""")
    cursor.execute("""
        INSERT into dbupdate(key, value)
        VALUES(?, ?)""", ("version", "ver0.002"))
    database.commit()

    #add new column to table [logs]
    cursor.execute("""
        ALTER TABLE logs ADD COLUMN gameat timestamp NOT NULL DEFAULT 0;
    """)
    cursor.execute("""
        ALTER TABLE logs ADD COLUMN rulecode char(4) NOT NULL DEFAULT '0000';
    """)
    cursor.execute("""
        ALTER TABLE logs ADD COLUMN lobby char(4) NOT NULL DEFAULT '0000';
    """)
    cursor.execute("""
        ALTER TABLE logs ADD COLUMN createat timestamp NOT NULL DEFAULT 0;
    """)
    database.commit()

    for row in cursor.execute(r"select ref from logs;").fetchall():
        ref = row[0]
        date = datetime.datetime.strptime(ref[0:10], "%Y%m%d%H")
        ruleCode = ref[13:17]
        lobby = ref[18:22]
        cursor.execute("""update logs set 
                                      gameat = ?,
                                      rulecode = ?, 
                                      lobby = ?, 
                                      createat = ? where ref = ?""", 
                      (date, ruleCode, lobby, date, ref))
    database.commit()

    #add new table for json API cache
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name char(40) NOT NULL,
            hash char(64) NOT NULL,
            json text NOT NULL
        );""")
    database.close()

    print "ok, database update to ver0.002."
elif version == "ver0.002":
    """
    var0.001 => ver0.002
    """

    database = sqlite3.connect(dbname)
    cursor = database.cursor()    

    errorLogs = list()
    for ref, jss in cursor.execute("""select ref, json from logs""").fetchall():
        try:
            js = json.loads(jss)
            sc = js["sc"]
        except Exception, e:
            errorLogs.append(ref)

    for ref in errorLogs:
        cursor.execute(r"delete from logs where ref = ?", (ref, ))
        cursor.execute(r"delete from logs_name where ref = ?", (ref, ))

    cursor.execute(r"update dbupdate set value = ? where key = ?",("version", "ver0.003"))
    database.commit()

    database.close()
    print "ok, database update to ver0.003."