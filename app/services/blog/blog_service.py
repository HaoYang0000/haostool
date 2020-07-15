from app.models.blog.post import BlogPostModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class BlogService(BaseService):
	model = BlogPostModel
	
	def get_posts_by_uuid(self, uuid: str):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.uuid==uuid).first()
	
	def update_by_uuid(self, uuid: str, title: str, content: str, is_published: bool=None, viewed_number: int=None, blog_intro: str=None, cover_img: str=None):
		with session_scope() as session:
			post = session.query(self.model).filter(self.model.uuid==uuid).first()
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
	
	def publish_blog(self, post_id):
		with session_scope() as session:
			blog = session.query(self.model).filter(self.model.id==post_id).first()
			blog.is_published = 1
			session.commit()
			return True

	def unpublish_blog(self, post_id):
		with session_scope() as session:
			blog = session.query(self.model).filter(self.model.id==post_id).first()
			blog.is_published = 0
			session.commit()
			return True