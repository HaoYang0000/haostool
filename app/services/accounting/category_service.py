from app.models.accounting.account_categories import AccountCategoryModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class CategoryService(BaseService):
	model = AccountCategoryModel

	def get_categories_for_user(self, user_id):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.user_id == user_id).all()