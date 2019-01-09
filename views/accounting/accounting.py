import logging

from controllers.accounting.main_controller import MainController as Controller
from flask import Blueprint, abort, make_response, request, redirect, url_for
from flask_api import status
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask import Blueprint, jsonify, render_template

logger = logging.getLogger('flask.app')

app = Blueprint(
    'accounting',
    __name__,
    url_prefix='/accounting'
)

@app.route('/', methods=['GET'])
def get_main_page():
	controller = Controller()

	weekly_cost = controller.get_weekly_cost()
	tags = controller.get_all_tags()
	categories = controller.get_all_categories()
	items = controller.get_all_items()
	return render_template('accounting/accounting.html', weekly_cost=weekly_cost, tags=tags, categories=categories, items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
	controller = Controller()
	item_name = request.form.get('item_name')
	item_price = request.form.get('item_price')
	item_date = request.form.get('item_date')
	tag_id = request.form.get('tag_id')
	controller.add_item(name=item_name, price=item_price, date=item_date, tag_id=tag_id)
	return redirect(url_for('accounting.get_main_page'))

@app.route('/add_tag', methods=['POST'])
def add_tag():
	controller = Controller()
	tag_name = request.form.get('tag_name')
	controller.add_tag(name=tag_name)
	return redirect(url_for('accounting.get_main_page'))

@app.route('/add_category', methods=['POST'])
def add_category():
	controller = Controller()
	category_name = request.form.get('category_name')
	tag_id = request.form.get('tag_id')
	controller.add_category(name=category_name, tag_id=tag_id)
	return redirect(url_for('accounting.get_main_page'))
