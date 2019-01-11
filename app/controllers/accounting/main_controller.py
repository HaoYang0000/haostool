import logging
from datetime import date, timedelta

from app.services.accounting.item_service import ItemService
from app.services.accounting.tag_service import TagService
from app.services.accounting.category_service import CategoryService
from app.schemas.accounting.account_items import AccountItemSchema
from app.schemas.accounting.account_tags import AccountTagSchema
from app.models.accounting.account_items import AccountItemModel
from app.models.accounting.account_tags import AccountTagModel
from app.models.accounting.account_categories import AccountCategoryModel

logger = logging.getLogger('flask.app')

class MainController:
	current_user = None
	item_service = None
	tag_service = None
	category_service = None

	def __init__(self, current_user):
		self.current_user = current_user
		self.item_service = ItemService()
		self.tag_service = TagService()
		self.category_service = CategoryService()
	
	def get_weekly_cost(self):
		my_date = date.today()
		start_of_week = my_date - timedelta(days=my_date.weekday())
		items = AccountItemModel.query.filter(AccountItemModel.date > start_of_week).filter(AccountItemModel.user_id == self.current_user.id).all()
		total_cost = 0

		for item in items:
			total_cost = total_cost + item.price
		return total_cost

	def get_all_items(self):
		return AccountItemModel.query.filter(AccountItemModel.user_id == self.current_user.id).all()

	def get_all_tags(self):
		return AccountTagModel.query.filter(AccountTagModel.user_id == self.current_user.id).all()

	def get_all_categories(self):
		return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == self.current_user.id).all()

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
		items = AccountItemModel.query.filter(AccountItemModel.date > start_of_week).filter(AccountItemModel.user_id == self.current_user.id).all()
		total_cost = 0

		for item in items:
			total_cost = total_cost + item.price
		return total_cost

	def get_cost_by_day(self, date):
		items = AccountItemModel.query.filter(AccountItemModel.date==date).filter(AccountItemModel.user_id == self.current_user.id).all()
		total_cost = 0
		for item in items:
			total_cost = total_cost + item.price
		return total_cost

	def get_cost_by_tag(self, tag_id):
		items = AccountItemModel.query.filter(AccountItemModel.tag_id==tag_id).filter(AccountItemModel.user_id == self.current_user.id).all()
		total_cost = 0
		for item in items:
			total_cost = total_cost + item.price
		return total_cost
