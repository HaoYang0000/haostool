from app.models.accounting.account_items import AccountItemModel
from app.models.accounting.account_tags import AccountTagModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class ItemService(BaseService):
	model = AccountItemModel

	def get_items_for_user(self, user_id):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.user_id == user_id).all()

	def get_items_for_user_before_time(self, user_id, time):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.date > time).filter(self.model.user_id == user_id).all()

	def get_items_by_tag_id(self, tag_id):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.tag_id == tag_id).all()