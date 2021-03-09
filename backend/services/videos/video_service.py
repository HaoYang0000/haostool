from backend.models.videos.video import VideoModel
from backend.services.base import BaseService
from sqlalchemy import asc
from backend.engine import db, session_scope, DEFAULT_PAGE_LIMIT


class VideoService(BaseService):
    model = VideoModel

    def get_videos(self, category: str, order: str, sort_by: str, page: int = 1, limit: int = DEFAULT_PAGE_LIMIT):
        offset = (page - 1) * limit
        order_by_attr = self.model.created_at
        if sort_by == 'Latest':
            order_by_attr = self.model.created_at
        elif sort_by == 'Most recommended':
            order_by_attr = self.model.star
        elif sort_by == 'Most viewed':
            order_by_attr = self.model.viewed_number
        elif sort_by == 'Most liked':
            order_by_attr = self.model.liked_number

        with session_scope() as session:
            query = session.query(self.model)
            if category == 'dota':
                query = query.filter(self.model.category == 'dota')
            elif category == 'pubg':
                query = query.filter(self.model.category == 'pubg')
            elif category == 'fallguys':
                query = query.filter(self.model.category == 'fallguys')
            elif category == 'piano':
                query = query.filter(self.model.category == 'piano')
            if order == 'asc':
                return query.order_by(order_by_attr.asc()).limit(limit).offset(offset).all()
            else:
                return query.order_by(order_by_attr.desc()).limit(limit).offset(offset).all()

    def get_total_page_len(self, category: str) -> int:
        with session_scope() as session:
            if category == 'all':
                return len(session.query(self.model).all())
            else:
                return len(session.query(self.model).filter(self.model.category == category).all())

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

    def increse_star(self, id):
        with session_scope() as session:
            video = session.query(self.model).filter(
                self.model.id == id).first()
            cur_num = video.star if video.star else 0
            video.star = cur_num + 1
            session.commit()
            return cur_num + 1

    def decrease_star(self, id):
        with session_scope() as session:
            video = session.query(self.model).filter(
                self.model.id == id).first()
            cur_num = video.star if video.star else 0
            video.star = cur_num - 1
            session.commit()
            return cur_num - 1

    def get_video_by_uuid(self, uuid: str):
        with session_scope() as session:
            video = session.query(self.model).filter(
                self.model.uuid == uuid).first()
            return video

    # def get_categories_for_user(self, user_id):
    # 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()
