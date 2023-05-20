#!/usr/bin/env bash

if [ "$(uname)" == "Darwin" ]; then
    source venv/bin/activate      
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    venv\Scripts\activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    venv\Scripts\activate
fi

python -m pip install -t lib -r .\requirements.txt