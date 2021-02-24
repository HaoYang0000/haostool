from backend.models.timelines.timeline import TimelineModel
from backend.services.base import BaseService
from sqlalchemy import asc
from backend.engine import db, session_scope


class TimelineService(BaseService):
    model = TimelineModel

    def get_all(self):
        with session_scope() as session:
            timelines = session.query(self.model).filter(
                self.model.is_removed.isnot(True)).order_by(self.model.created_at.desc()).all()
            return timelines

    def deactive_timeline(self, id):
        with session_scope() as session:
            timeline = session.query(self.model).filter(
                self.model.id == id).first()
            timeline.is_removed = 1
            session.commit()
            return True

    # def _like_increase(self, video):
    # 	with session_scope() as session:
    # 		video.liked_number = video.liked_number + 1
    # 		session.merge(video)
    # 		session.commit()
    # 		return

    # def get_categories_for_user(self, user_id):
    # 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()
