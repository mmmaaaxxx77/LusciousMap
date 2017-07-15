#!/bin/bash
# 100

# mysql
service mysql stop

service mysql start
service mysql start
service mysql start

# 清除所有screen 
screen -wipe
screen -ls | grep -i detached | cut -d. -f1 | tr -d [:blank:]| xargs kill
#screen -ls | grep pts | cut -d. -f1 | awk '{print $1}' | xargs kill

source /vm/Django1.10.6/bin/activate && cd /home/analysis//LusciousMap/LusciousMap
python3 manage.py runserver 0.0.0.0:8000
