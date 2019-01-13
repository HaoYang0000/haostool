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
		start_of_week = date.today() - timedelta(days=date.today().weekday())
		start_of_week = start_of_week.strftime('%Y%m%d') + "000000"
		items = self.item_service.get_items_for_user_before_time(user_id=self.current_user.id, time=start_of_week)
		return self.__get_total_cost(items)

	def get_monthly_cost(self):
		start_of_month = date.today().replace(day=1).strftime('%Y%m%d') + "000000"
		items = self.item_service.get_items_for_user_before_time(user_id=self.current_user.id, time=start_of_month)
		return self.__get_total_cost(items)

	def get_daily_cost(self):
		start_of_day = date.today().strftime('%Y%m%d') + "000000"
		items = self.item_service.get_items_for_user_before_time(user_id=self.current_user.id, time=start_of_day)
		return self.__get_total_cost(items)

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

	def get_cost_by_tag(self, tag_id):
		pass
	def __get_total_cost(self, items):
		total_cost = 0.0
		for item in items:
			total_cost = total_cost + item.price
		return total_cost
