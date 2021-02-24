from backend.models.users.users import UserModel
from backend.services.base import BaseService
from sqlalchemy import asc
from backend.engine import session_scope


class UserService(BaseService):
    model = UserModel

    # def get_service_from_user(self, user_id):
    #     """
    #     Return api list result

    #     Returns:
    #         model | null
    #     """
    #     with session_scope() as session:
    #         return session.query(self.model).filter(self.model.user_id == user_id).all()

    # def get_services_from_ids(self, ids):
    #     with session_scope() as session:
    #         return [session.query(self.model).filter(self.model.id == id).one() for id in ids]
