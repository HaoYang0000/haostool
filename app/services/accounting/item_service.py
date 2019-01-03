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