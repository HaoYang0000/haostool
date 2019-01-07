from models.accounting.account_tags import AccountTagModel
from services.base import BaseService
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