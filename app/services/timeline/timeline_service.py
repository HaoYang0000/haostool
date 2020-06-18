from app.models.timeline.timeline import TimelineModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import db, session_scope


class TimelineService(BaseService):
	model = TimelineModel

	# def _like_increase(self, video):
	# 	with session_scope() as session:
	# 		video.liked_number = video.liked_number + 1
	# 		session.merge(video)
	# 		session.commit()
	# 		return
	
    # def get_categories_for_user(self, user_id):
    # 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()
