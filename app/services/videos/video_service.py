from app.models.videos.video import VideoModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import db, session_scope


class VideoService(BaseService):
	model = VideoModel

	def get_all_videos_created_desc(self):
		with session_scope() as session:
			return session.query(self.model).order_by(self.model.created_at.desc()).all()


	def _like_increase(self, video):
		with session_scope() as session:
			video.liked_number = video.liked_number + 1
			session.merge(video)
			session.commit()
			return
	
	def _view_increase(self, video):
		with session_scope() as session:
			video.viewed_number = video.viewed_number + 1
			session.merge(video)
			session.commit()
			return

	def get_video_by_uuid(self, uuid: str):
		with session_scope() as session:
			video = session.query(self.model).filter(self.model.uuid == uuid).first()
			return video

    # def get_categories_for_user(self, user_id):
    # 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()
