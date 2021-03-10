from backend.models.labels.label import LabelModel
from backend.models.labels.label_bridge import LabelBridgeModel
from backend.services.base import BaseService
from sqlalchemy import asc
from backend.engine import db, session_scope


class LabelService(BaseService):
    model = LabelModel

    def create_label_for_blog(self, label_id: int, blog_id: int):
        with session_scope() as session:
            new_label_blog_bridge = LabelBridgeModel(
                label_id=label_id,
                blog_id=blog_id
            )
            session.add(new_label_blog_bridge)
            session.commit()
            return "Create blog label success"

    def delete_label_for_blog(self, label_id: int, blog_id: int):
        with session_scope() as session:
            record = session.query(LabelBridgeModel).filter(LabelBridgeModel.blog_id == blog_id).filter(
                LabelBridgeModel.label_id == label_id).one()
            session.delete(record)
            session.commit()
            return "Delete blog label success"

    def create_label_for_video(self, label_id: int, video_id: int):
        with session_scope() as session:
            new_label_video_bridge = LabelBridgeModel(
                label_id=label_id,
                video_id=video_id
            )
            session.add(new_label_video_bridge)
            session.commit()
            return "Create video label success"

    def delete_label_for_video(self, label_id: int, video_id: int):
        with session_scope() as session:
            record = session.query(LabelBridgeModel).filter(LabelBridgeModel.video_id == video_id).filter(
                LabelBridgeModel.label_id == label_id).one()
            session.delete(record)
            session.commit()
            return "Delete video label success"
    # def get_categories_for_user(self, user_id):
    # 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()
