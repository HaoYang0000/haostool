import logging
from datetime import date, timedelta

from services.accounting.item_service import ItemService
from services.accounting.tag_service import TagService
from services.accounting.category_service import CategoryService
from schemas.accounting.account_items import AccountItemSchema
from schemas.accounting.account_tags import AccountTagSchema
from models.accounting.account_items import AccountItemModel

logger = logging.getLogger('flask.app')

class MainController:
	item_service = ItemService()
	tag_service = TagService()
	category_service = CategoryService()

	def __init__(self):
		pass
	
	def get_weekly_cost(self):
		my_date = date.today()
		start_of_week = my_date - timedelta(days=my_date.weekday())
		items = AccountItemModel.query.filter(AccountItemModel.date > start_of_week).all()
		total_cost = 0

		for item in items:
			total_cost = total_cost + item.price
		return total_cost

	def get_all_items(self):
		return self.item_service.get_all()

	def get_all_tags(self):
		return self.tag_service.get_all()

	def get_all_categories(self):
		return self.category_service.get_all()

	def add_item(self, **kwargs):
		self.item_service.create(**kwargs)
		return True

	def add_tag(self, **kwargs):
		self.tag_service.create(**kwargs)
		return True

	def add_category(self, **kwargs):
		self.category_service.create(**kwargs)
		return True

	def get_monthly_cost(self):
		my_date = date.today().replace(day=1)
		items = AccountItemModel.query.filter(AccountItemModel.date > start_of_week).all()
		total_cost = 0

		for item in items:
			total_cost = total_cost + item.price
		return total_cost

	def get_cost_by_day(self, date):
		items = AccountItemModel.query.filter(AccountItemModel.date==date).all()
		total_cost = 0
		for item in items:
			total_cost = total_cost + item.price
		return total_cost

	def get_cost_by_tag(self, tag_id):
		items = AccountItemModel.query.filter(AccountItemModel.tag_id==tag_id).all()
		total_cost = 0
		for item in items:
			total_cost = total_cost + item.price
		return total_cost
