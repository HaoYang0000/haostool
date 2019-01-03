import logging

from app.services.accounting.item_service import ItemService
from app.services.accounting.tag_service import TagService
from app.services.accounting.category_service import CategoryService
from app.schemas.accounting.account_items import AccountItemSchema
from app.schemas.accounting.account_tags import AccountTagSchema

logger = logging.getLogger('flask.app')

class MainController:
	item_service = ItemService()
	tag_service = TagService()
	category_service = CategoryService()

	def __init__(self):
		pass
	
	def get_weekly_cost(self):
		items = self.item_service.get_all()

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
		pass

	def get_yesterday_cost(self):
		pass

	def get_cost_by_day(self):
		pass

	def get_cost_by_tag(self):
		pass

	def get_cost_by_time_range(self):
		pass
