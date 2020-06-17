from app.models.comment import CommentModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import db, session_scope


class CommentService(BaseService):
	model = CommentModel

	# def _like_increase(self, video):
	# 	with session_scope() as session:
	# 		video.liked_number = video.liked_number + 1
	# 		session.merge(video)
	# 		session.commit()
	# 		return

	def get_reply_for_video_uuid(self, video_uuid):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.video_uuid==video_uuid).order_by(self.model.created_at.desc()).all()
	
	def get_all_feedback_comment(self):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.category=='feedback').order_by(self.model.created_at.desc()).all()

    # def get_categories_for_user(self, user_id):
    # 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()
