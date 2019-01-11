import logging
from datetime import date, timedelta
from app.models.services import ServiceModel
from app.models.user_service import UserServiceModel

logger = logging.getLogger('flask.app')

class MainController:
	current_user = None

	def __init__(self, current_user):
		self.current_user = current_user
	
	def get_all_service(self):
		services = UserServiceModel.query.filter(UserServiceModel.user_id==self.current_user.id).all()
		ids = []
		for service in services:
			ids.append(service.service_id)
		filtered_service = [ServiceModel.query.filter(ServiceModel.id==id).one() for id in ids]
		return filtered_service

