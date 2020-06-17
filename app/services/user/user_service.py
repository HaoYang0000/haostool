from app.models.users import UserModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class UserService(BaseService):
    model = UserModel