#! /bin/bash
cd /var/www/haostool
source ./env/bin/activate
exec /usr/bin/gunicorn -b localhost:8080 -w 4 main:app