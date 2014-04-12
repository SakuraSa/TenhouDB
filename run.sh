#!/bin/sh
git pull https://github.com/ChocoProject/TenhouDB.git matser
nohup python index.py 0.0.0.0:80 2>&1 &