from app.models.blog.post import BlogPostModel
from app.services.base import BaseService
from sqlalchemy import asc
from app.engine import session_scope


class BlogService(BaseService):
	model = BlogPostModel
	
	def get_posts_by_uuid(self, uuid: str):
		with session_scope() as session:
			return session.query(self.model).filter(self.model.uuid==uuid).first()
	
	def update_by_uuid(self, uuid: str, title: str, content: str, is_published: bool=None, viewed_number: int=None):
		with session_scope() as session:
			post = session.query(self.model).filter(self.model.uuid==uuid).first()
			new_data = {}
			new_data['title'] = title
			new_data['content'] = content
			if is_published:
				new_data['is_published'] = is_published
			if viewed_number:
				new_data['viewed_number'] = viewed_number
			return self.update_by_id(
				id=post.id,
				data=new_data
			)

	# def get_categories_for_user(self, user_id):
	# 	return AccountCategoryModel.query.filter(AccountCategoryModel.user_id == user_id).all()