#!/usr/bin/env bash
virtualenv env

if [ "$(uname)" == "Darwin" ]; then
    source env/bin/activate      
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    source env/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    env\Scripts\activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    env\Scripts\activate
fi

python -m pip install -t lib -r .\requirements.txt