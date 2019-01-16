from app.models.accounting.account_items import AccountItemModel
from app.models.accounting.account_tags import AccountTagModel
from app.services.base import BaseService
from sqlalchemy import asc


class ItemService(BaseService):
	model = AccountItemModel

	def get_all(self, **kwargs):
		"""
        Return api list result

        Returns:
        model | null
        """
		return self.model.query.all()

	def get_items_for_user(self, user_id):
		return AccountItemModel.query.filter(AccountItemModel.user_id == user_id).all()

	def get_items_for_user_before_time(self, user_id, time):
		return AccountItemModel.query.filter(AccountItemModel.date > time).filter(AccountItemModel.user_id == user_id).all()

	def get_items_by_tag_id(self, tag_id):
		return AccountItemModel.query.filter(AccountItemModel.tag_id == tag_id).all()