import logging
import json

from app.controllers.accounting.main_controller import MainController as Controller
from flask import Blueprint, abort, make_response, request, redirect, url_for, flash
from flask_api import status
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from flask_login import current_user, login_user, logout_user
from app.forms.accounting.accounting_form import AddItemForm, AddTagForm, AddItemForm, AddCategoryForm
from app.services.accounting.tag_service import TagService
from app.schemas.accounting.account_tags import AccountTagSchema

logger = logging.getLogger('flask.app')

app = Blueprint(
    'accounting',
    __name__,
    url_prefix='/accounting'
)

controller = Controller(current_user=current_user)

@app.route('/', methods=['GET'])
@login_required
def get_main_page():
	all_tags = TagService().get_all()

	add_item_form = AddItemForm()
	add_tag_form = AddTagForm()
	add_category_form = AddCategoryForm()
	add_item_form.tag_id.choices = [(tag.id, tag.name) for tag in all_tags]

	daily_cost = controller.get_daily_cost()
	weekly_cost = controller.get_weekly_cost()
	monthly_cost = controller.get_monthly_cost()

	tags = controller.get_all_tags()
	for tag in tags:
		tag.cost = controller.get_cost_by_tag(tag.id) 
	
	categories = controller.get_all_categories()
	items = controller.get_all_items()

	return render_template('accounting/accounting.html', 
		daily_cost=daily_cost, 
		weekly_cost=weekly_cost, 
		monthly_cost=monthly_cost, 
		tags=tags, 
		tag_cost=AccountTagSchema(many=True).dumps(tags).data,
		categories=categories, 
		items=items,
		add_item_form=add_item_form,
		add_tag_form=add_tag_form,
		add_category_form=add_category_form
	)

@app.route('/cost_by_tag/<int:tag_id>', methods=['GET'])
@login_required
def cost_by_tag(tag_id):
	cost = controller.get_cost_by_tag(tag_id)
	return jsonify(cost)


@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
	add_item_form = AddItemForm()
	all_tags = TagService().get_all()
	add_item_form.tag_id.choices = [(tag.id, tag.name) for tag in all_tags]
	if add_item_form.validate_on_submit():
		item_name = add_item_form.item_name.data
		item_price = add_item_form.item_price.data
		item_date = add_item_form.item_date.data
		tag_id = add_item_form.tag_id.data
		user_id = current_user.id
		controller.add_item(name=item_name, price=item_price, date=item_date, tag_id=tag_id, user_id=user_id)
	return redirect(url_for('accounting.get_main_page'))


@app.route('/add_tag', methods=['POST'])
@login_required
def add_tag():
	add_tag_form = AddTagForm()
	if add_tag_form.validate_on_submit():
		tag_name = add_tag_form.tag_name.data
		user_id = current_user.id
		controller.add_tag(name=tag_name, user_id=user_id)
	return redirect(url_for('accounting.get_main_page'))


@app.route('/add_category', methods=['POST'])
@login_required
def add_category():
	add_category_form = AddCategoryForm()
	if add_category_form.validate_on_submit():
		category_name = add_category_form.category_name.data
		tag_id = add_category_form.tag_id.data
		user_id = current_user.id
		controller.add_category(name=category_name, tag_id=tag_id, user_id=user_id)
	return redirect(url_for('accounting.get_main_page'))
