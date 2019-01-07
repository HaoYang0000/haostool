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




class AccountingList(MethodResource):
    

    def get(self, **kwargs):
    	pass

    # @use_kwargs(NotificationLogSchema().fields)
    # @marshal_with(NotificationLogSchema, code=status.HTTP_201_CREATED)
    # def post(self, **kwargs):
    #     validation = self.log_service.validate_foreign_key(**kwargs)
    #     if validation is False:
    #         abort(status.HTTP_400_BAD_REQUEST)
    #     new_log = self.log_service.create(**kwargs)
    #     return new_log, status.HTTP_201_CREATED


class ItemDetail(MethodResource):
	pass



# add_url_rule(
#     '',
#     view_func=AccountingList.as_view('AccountingList'),
#     methods=['GET', 'POST']
# )
app.add_url_rule(
    '/<int:item_id>',
    view_func=ItemDetail.as_view('ItemDetail'),
    methods=['GET', 'PUT', 'DELETE', 'PATCH']
)
