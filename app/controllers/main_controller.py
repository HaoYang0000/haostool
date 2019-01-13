import logging
from datetime import date, timedelta
from app.services.user_service import UserService

logger = logging.getLogger('flask.app')

class MainController:
	current_user = None
	user_service = None

	def __init__(self, current_user):
		self.current_user = current_user
		self.user_service = UserService()
	
	def get_all_service(self):
		services = self.user_service.get_service_from_user(user_id=self.current_user.id)
		ids = []
		for service in services:
			ids.append(service.service_id)
		filtered_service = self.user_service.get_services_from_ids(ids=ids)
		return filtered_service

