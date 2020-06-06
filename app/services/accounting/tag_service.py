from app.models.accounting.account_tags import AccountTagModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class TagService(BaseService):
    model = AccountTagModel

    def get_tags_for_user(self, user_id):
        with session_scope as session:
    	    return session.query(self.model).filter(self.model.user_id == user_id).all()