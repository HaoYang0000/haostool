from app.models.videos.video import VideoModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import db


class VideoService(BaseService):
	model = VideoModel

	def get_all_videos(self, **kwargs):
		"""
		Return api list result

		Returns:
			model | null
		"""
		return self.model.query.all()

	def _like_increase(self, video):
		video.liked_number = video.liked_number + 1
		# db.session.merge(video)
		db.session.commit()
		return
	
	def _view_increase(self, video):
		video.viewed_number = video.viewed_number + 1
		# db.session.merge(video)
		# db.session.flush()
		db.session.commit()
		return

	def get_video_by_uuid(self, uuid: str):
		video = self.model.query.filter(VideoModel.uuid == uuid).first()
		return video

    # def get_categories_for_user(self, user_id):
    # 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()
