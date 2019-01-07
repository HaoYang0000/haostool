from models.accounting.account_categories import AccountCategoryModel
from services.base import BaseService
from sqlalchemy import asc


class CategoryService(BaseService):
    model = AccountCategoryModel

    def get_all(self, **kwargs):
        """
        Return api list result

        Returns:
            model | null
        """
        return self.model.query.all()