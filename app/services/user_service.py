from app.models.services import ServiceModel
from app.models.user_service import UserServiceModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class UserService(BaseService):
    model = UserServiceModel

    def get_service_from_user(self, user_id):
        """
        Return api list result

        Returns:
            model | null
        """
        with session_scope() as session:
            return session.query(self.model).filter(self.model.user_id==user_id).all()

    def get_services_from_ids(self, ids):
        with session_scope() as session:
    	    return [session.query(self.model).filter(self.model.id==id).one() for id in ids]