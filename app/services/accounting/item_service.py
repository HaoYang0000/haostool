from app.models.accounting import AccountItemModel
from app.models.accounting import AccountTagModel
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
        return self.model.query.filter_by(**kwargs).order_by(asc(self.model.order)).all()