#!/bin/sh
git pull https://github.com/SakuraSa/TenhouDB.git master
nohup python index.py 0.0.0.0:80 2>&1 &