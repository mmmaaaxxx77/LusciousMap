#!/bin/bash
# 100

# mysql
service mysql stop
# redis-server
#service redis-server start

service mysql start
service mysql start

#screen -L -t Django -dmS Django bash -c 'source /vm/Django1.10.6/bin/activate && cd /home/analysis/VTT && python3 manage.py runserver 0.0.0.0:8000'
