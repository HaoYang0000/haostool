from app.models.users import UserModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class UserService(BaseService):
    model = UserModel
        
    def is_admin(self, user_id):
        with session_scope() as session:
            user = session.query(self.model).filter(self.model.id==user_id).one()
            return user.level <= 1