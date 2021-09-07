from backend.models.blogs.post import BlogPostModel, HiddenContentModel, HiddenContentBridgeModel
from backend.models.labels.label import LabelModel
from backend.models.labels.label_bridge import LabelBridgeModel
from backend.services.base import BaseService
from backend.logs.logger import logger
from sqlalchemy import asc
from backend.engine import session_scope, DEFAULT_PAGE_LIMIT


class BlogService(BaseService):
    model = BlogPostModel

    def get_blogs(self, order: str, label: str, sort_by: str, page: int = 1, limit: int = DEFAULT_PAGE_LIMIT):
        offset = (page - 1) * limit
        order_by_attr = self.model.created_at
        if sort_by == 'Latest':
            order_by_attr = self.model.created_at
        elif sort_by == 'Most viewed':
            order_by_attr = self.model.viewed_number
        elif sort_by == 'Most liked':
            order_by_attr = self.model.liked_number

        with session_scope() as session:
            query = session.query(self.model)
            if label:
                query = query.join(LabelBridgeModel, LabelBridgeModel.blog_id == self.model.id).join(
                    LabelModel, LabelModel.id == LabelBridgeModel.label_id).filter(LabelModel.name.in_(label.split(",")))
            if order == 'asc':
                return query.order_by(order_by_attr.asc()).limit(limit).offset(offset).all()
            else:
                return query.order_by(order_by_attr.desc()).limit(limit).offset(offset).all()

    def get_all_published_blogs(self):
        with session_scope() as session:
            return session.query(self.model).filter(self.model.is_published == True).all()

    def get_posts_by_uuid(self, uuid: str):
        with session_scope() as session:
            return session.query(self.model).filter(self.model.uuid == uuid).first()

    def update_by_uuid(self, uuid: str, title: str, content: str, is_hidden: bool, is_published: bool = None, viewed_number: int = None, blog_intro: str = None, cover_img: str = None):
        with session_scope() as session:
            post = session.query(self.model).filter(
                self.model.uuid == uuid).first()
            new_data = {}
            new_data['title'] = title
            new_data['content'] = content
            new_data['is_hidden'] = True if is_hidden and is_hidden.lower(
            ) == 'true' else False
            if blog_intro:
                new_data['blog_intro'] = blog_intro
            if cover_img:
                new_data['cover_img'] = cover_img
            if is_published:
                new_data['is_published'] = is_published
            if viewed_number:
                new_data['viewed_number'] = viewed_number
            return self.update_by_id(
                id=post.id,
                data=new_data
            )

    def like_increase(self, blog):
        with session_scope() as session:
            blog.liked_number = blog.liked_number + 1
            session.merge(blog)
            session.commit()
            return

    def view_increase(self, blog):
        with session_scope() as session:
            blog.viewed_number = blog.viewed_number + 1
            session.merge(blog)
            session.commit()
            return

    def publish_blog(self, blog_id):
        with session_scope() as session:
            blog = session.query(self.model).filter(
                self.model.id == blog_id).first()
            blog.is_published = 1
            session.commit()
            return True

    def unpublish_blog(self, blog_id):
        with session_scope() as session:
            blog = session.query(self.model).filter(
                self.model.id == blog_id).first()
            blog.is_published = 0
            session.commit()
            return True

    def update_hidden_content_config(self, id: int, name: str, uuid: str):
        with session_scope() as session:
            post = session.query(HiddenContentModel).filter(
                HiddenContentModel.id == id)
            new_data = {}
            new_data['name'] = name
            new_data['uuid'] = uuid
            post.update(new_data)
            session.commit()
            return "success"

    def hidden_blog(self, blog_id):
        with session_scope() as session:
            blog = session.query(self.model).filter(
                self.model.id == blog_id).first()
            blog.is_hidden = 1
            session.commit()
            return True

    def unhidden_blog(self, blog_id):
        with session_scope() as session:
            blog = session.query(self.model).filter(
                self.model.id == blog_id).first()
            blog.is_hidden = 0
            session.commit()
            return True

    def get_all_hidden_content_categories(self):
        with session_scope() as session:
            categories = session.query(HiddenContentModel).all()
            return categories

    def create_hidden_content_category(self, name: str, uuid: str):
        with session_scope() as session:
            new_hidden_content_category = HiddenContentModel(
                name=name,
                uuid=uuid
            )
            session.add(new_hidden_content_category)
            session.commit()
            return "Create hidden content category success"

    def delete_hidden_content_category_by_id(self, id: int):
        with session_scope() as session:
            record = session.query(HiddenContentModel).filter(
                HiddenContentModel.id == id).one()
            session.delete(record)
            session.commit()
            return "Delete hidden content categorysuccess"

    def get_all_hidden_blogs(self):
        with session_scope() as session:
            return session.query(self.model).filter(self.model.is_hidden == True).all()

    def get_hidden_blogs_by_hidden_bridge_uuid(self, uuid: str):
        with session_scope() as session:
            hidden_content = session.query(HiddenContentModel).filter(
                HiddenContentModel.uuid == uuid).one()
            outputs = [blog.serialize for blog in hidden_content.blogs]
            logger.info(outputs)
            return outputs

    def link_hidden_category_with_blog(self, blog_id: int, hidden_content_id: int):
        with session_scope() as session:
            new_hidden_content_blog_bridge = HiddenContentBridgeModel(
                blog_id=blog_id,
                hidden_content_id=hidden_content_id
            )
            session.add(new_hidden_content_blog_bridge)
            session.commit()
            return "add blog to hidden content category success"

    def unlink_hidden_category_with_blog(self, blog_id: int, hidden_content_id: int):
        with session_scope() as session:
            record = session.query(HiddenContentBridgeModel).filter(HiddenContentBridgeModel.blog_id == blog_id).filter(
                HiddenContentBridgeModel.hidden_content_id == hidden_content_id).first()
            session.delete(record)
            session.commit()
            return "Delete blog to hidden content category success"

    def get_hidden_content(self):
        pass
