#! /bin/bash
cd /var/www/haostool
source ./env/bin/activate
/usr/bin/gunicorn -b localhost:8080 -w 4 main:app