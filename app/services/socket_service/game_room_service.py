from app.models.socket_service.game_room import GameRoomModel
from app.services.base import BaseService
from sqlalchemy import asc


class GameRoomService(BaseService):
	model = GameRoomModel

	def get_all(self, **kwargs):
		"""
        Return api list result

        Returns:
            model | null
        """
		return self.model.query.all()

	# def get_categories_for_user(self, user_id):
	# 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()