import json
import logging

from flask import Blueprint, jsonify, render_template
from flask_api import status

app = Blueprint('index', __name__)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET', 'POST'])
def health():
    return 'OK', status.HTTP_201_CREATED


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/<whatever>/<int:times>', methods=['GET', 'POST'])
def lol(whatever, times):
	return_list = []
	for x in range(times):
		return_list.append(whatever)

	return render_template('whatever.html', whatever=return_list)

@app.errorhandler(Exception)
def exception_handler(error):
    return "!!!!"  + repr(error)
