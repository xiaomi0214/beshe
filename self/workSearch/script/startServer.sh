#!/bin/bash 
dir=/mnt/hgfs/centos_share/python/auto_python/other_peaple/self/workSearch
cd $dir

curdate=`/usr/bin/date  "+%Y-%m-%d" `
echo $curdate

echo $1
echo "worker_"$curdate
echo logs/"flower"$curdate
#/root/.virtualenvs/py3/bin/uwsgi  --ini  other/uwsgi.ini

/root/.virtualenvs/py3/bin/python manage.py celery worker -c $1 --loglevel=info &>logs/"worker_"$curdate  &

/root/.virtualenvs/py3/bin/python manage.py  celery  flower  --address=127.0.0.1  --port=10001  --loglevel=info &>logs/"flower_"$curdate  &
