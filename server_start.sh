#! /bin/bash
cd /var/www/haostool
source ./env/bin/activate
gunicorn -b localhost:8080 -w 8 main:backend