from backend.models.blogs.post import BlogPostModel
from backend.services.base import BaseService
from sqlalchemy import asc
from backend.engine import session_scope, DEFAULT_PAGE_LIMIT


class BlogService(BaseService):
    model = BlogPostModel

    def get_blogs(self, order: str, sort_by: str, page: int = 1, limit: int = DEFAULT_PAGE_LIMIT):
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

    def update_by_uuid(self, uuid: str, title: str, content: str, is_published: bool = None, viewed_number: int = None, blog_intro: str = None, cover_img: str = None):
        with session_scope() as session:
            post = session.query(self.model).filter(
                self.model.uuid == uuid).first()
            new_data = {}
            new_data['title'] = title
            new_data['content'] = content
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
