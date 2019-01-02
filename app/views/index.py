import json
import logging

from flask import Blueprint, jsonify, render_template
from flask_api import status

from app.services.accounting.tag_service import TagService

app = Blueprint('index', __name__)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET', 'POST'])
def health():
    return 'OK', status.HTTP_201_CREATED


@app.route('/', methods=['GET', 'POST'])
def index():
	tag_service = TagService()
	tags = tag_service.get_all()
	return render_template('accounting/accounting.html', tags=tags)
