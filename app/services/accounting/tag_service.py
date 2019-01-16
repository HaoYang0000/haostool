from app.models.accounting.account_tags import AccountTagModel
from app.services.base import BaseService
from sqlalchemy import asc


class TagService(BaseService):
    model = AccountTagModel

    def get_all(self, **kwargs):
        """
        Return api list result

        Returns:
            model | null
        """
        return self.model.query.all()

    def get_tags_for_user(self, user_id):
    	return AccountTagModel.query.filter(AccountTagModel.user_id == user_id).all()