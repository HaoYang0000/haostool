# scan
pybabel extract -F babel.cfg  -o messages.pot .

# init 
pybabel init -i messages.pot -d app/translations -l zh_CN

# update
pybabel update -i messages.pot -d app/translations

# compile
pybabel compile -d app/translations 