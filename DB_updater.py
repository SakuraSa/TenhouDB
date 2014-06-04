#!/usr/bin/env python
#coding=utf-8


import datetime
import sqlite3
import os
import shutil
import json

lastVersion = "ver0.006"

dbname    = "tenhou.db"
tempfile  = "temp.db"
backupDir = "DBbackup"
version   = "ver0.001"
database  = sqlite3.connect(dbname)
cursor    = database.cursor()

#get database version and do backup
if cursor.execute(r"SELECT COUNT(*) as CNT FROM sqlite_master where type='table' and name='dbupdate';").fetchall()[0][0]:
    version = cursor.execute(r"SELECT value FROM dbupdate where key='version' limit 1").fetchall()[0][0]
if version == lastVersion:
    print "Database is last version: %s." % version
else:
    if not os.path.exists(backupDir):
        os.mkdir(backupDir)
    backupName = datetime.datetime.now().strftime("%Y%m%d%H%M%S.bk." + version)
    backupPath = os.path.join(backupDir, backupName)
    shutil.copyfile(dbname, backupPath)
    print "Backup DB to", backupPath, "whit %d logs" % cursor.execute(r'select COUNT(*) as CNT from logs').fetchall()[0][0]
    database.close()

    while version != lastVersion:
        #database update process
        if version == "ver0.001":
            """
            ver0.001 => ver0.002
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

            #add new table for json API cache
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS statistics_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name char(40) NOT NULL,
                    hash char(64) NOT NULL,
                    json text NOT NULL
                );""")
            database.commit()
            database.close()
            version = "ver0.002"
            print "ok, database update to ver0.002."
        elif version == "ver0.002":
            """
            ver0.002 => ver0.003
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

            cursor.execute(r"update dbupdate set value = ?, attime = ? where key = ?",
                ("ver0.003", datetime.datetime.now(), "version"))
            database.commit()
            database.close()
            version = 'ver0.003'
            print "ok, database update to ver0.003."
        elif version == "ver0.003":
            """
            ver0.003 => ver0.004
            """

            database = sqlite3.connect(dbname)
            cursor = database.cursor() 

            cursor.execute(r"ALTER TABLE statistics_cache ADD updated INTEGER DEFAULT 1")

            cursor.execute(r"update dbupdate set value = ?, attime = ? where key = ?",
                ("ver0.004", datetime.datetime.now(), "version"))
            database.commit()
            database.close()
            version = 'ver0.004'
            print "ok, database update to ver0.004."
        elif version == "ver0.004":
            """
            ver0.004 => ver0.005
            """

            database = sqlite3.connect(dbname)
            cursor = database.cursor() 

            cursor.execute(r"ALTER TABLE statistics_cache ADD global boolean DEFAULT false")

            cursor.execute(r"update dbupdate set value = ?, attime = ? where key = ?",
                ("ver0.005", datetime.datetime.now(), "version"))

            bans = [u"0841"]
            counter = 0
            for row in cursor.execute(r"select ref, rulecode from logs").fetchall():
                ref, rulecode = row
                if rulecode in bans:
                    cursor.execute(r"delete from logs where ref = ?", (ref, ))
                    cursor.execute(r"delete from logs_name where ref = ?", (ref, ))
                    counter += 1
                    print "info: [%4d] remove dirty data [%s]" % (counter, ref), rulecode

            database.commit()
            database.close()
            version = 'ver0.005'
            print "ok, database update to ver0.005."
        elif version == "ver0.005":
            """
            ver0.005 => ver0.006
            """

            import json
            database = sqlite3.connect(dbname)
            cursor = database.cursor() 

            cursor.execute(r"ALTER TABLE logs_name ADD sex char(1) DEFAULT 'M'")
            cursor.execute(r"ALTER TABLE logs_name ADD rate float DEFAULT 1500")
            cursor.execute(r"ALTER TABLE logs_name ADD dan char(16) DEFAULT 'unknow'")
            cursor.execute(r"ALTER TABLE logs_name ADD score INTEGER DEFAULT 0")
            cursor.execute(r"ALTER TABLE logs_name ADD point INTEGER DEFAULT 0")

            allLogs = dict()
            for row in cursor.execute(r"SELECT ref, json from logs").fetchall():
                allLogs[row[0]] = json.loads(row[1])

            for row in cursor.execute(r"SELECT ref, name from logs_name").fetchall():
                ref, name = row
                js = allLogs[ref]
                playerIndex = 0
                for i in range(len(js['name'])):
                    if js['name'][i] == name:
                        playerIndex = i
                        break
                sex = js['sx'][playerIndex]
                rate = js['rate'][playerIndex]
                dan = js['dan'][playerIndex]
                score = js['sc'][playerIndex * 2]
                point = js['sc'][playerIndex * 2 + 1]
                cursor.execute(r"UPDATE logs_name SET sex = ?, rate = ?, dan = ?, score = ?, point = ? WHERE ref = ? AND name = ?",
                    (sex, rate, dan, score, point, ref, name))

            cursor.execute(r"update dbupdate set value = ?, attime = ? where key = ?",
                ("ver0.006", datetime.datetime.now(), "version"))

            database.commit()
            database.close()

            version = 'ver0.006'
            print "ok, database update to ver0.006."