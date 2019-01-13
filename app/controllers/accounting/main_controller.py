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
		items = self.item_service.get_items_for_user_before_time(user_id=self.current_user.id, time=start_of_week)
		total_cost = 0

		for item in items:
			total_cost = total_cost + item.price
		return total_cost

	def get_all_items(self):
		return self.item_service.get_items_for_user(user_id=self.current_user.id)

	def get_all_tags(self):
		return self.tag_service.get_tags__for_user(user_id=self.current_user.id)

	def get_all_categories(self):
		return self.category_service.get_categories__for_user(user_id=self.current_user.id)

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
		pass

	def get_cost_by_day(self, date):
		pass

	def get_cost_by_tag(self, tag_id):
		pass
