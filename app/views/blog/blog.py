import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash
from flask_api import status
from flask_login import current_user, login_user, logout_user, login_required
from app.services.blog.blog_service import BlogService
from app.forms.blog.create_post_form import CreateBlogPostForm
import uuid
import pickle

app = Blueprint(
    'blog',
    __name__,
    url_prefix='/blog'
)
logger = logging.getLogger(__name__)

blog_service = BlogService()
SINGLE_QUOTE = '__SINGLE_QUOTE__'

@app.route('/', methods=['GET'])
def blogs():
    posts = BlogService().get_all()
    return render_template('blog/blog.html', posts=posts)

@app.route('/view/<string:uuid>', methods=['GET'])
def view_blogs(uuid):
    post = BlogService().get_posts_by_uuid(uuid=uuid)
    content = __format_str(post.content)
    return render_template('blog/view_blog.html', post=post, content=content)

@app.route('/edit/<string:uuid>', methods=['GET'])
@login_required
def edit_post(uuid):
    post = BlogService().get_posts_by_uuid(uuid=uuid)
    content = __format_str(post.content)
    form = CreateBlogPostForm()
    return render_template('blog/edit_post.html', post=post, form=form, content=content)

@app.route('/edit/<string:uuid>', methods=['POST'])
@login_required
def update_post(uuid):
    form = CreateBlogPostForm()
    if form.validate_on_submit():
        content=form.content.data
        post = BlogService().update_by_uuid(
            uuid=uuid,
            title=form.title.data,
            content=content
        )
        content = __format_str(post.content)
    return render_template('blog/edit_post.html', post=post, form=form, content=content)

@app.route('/create_post', methods=['GET'])
@login_required
def create_post_main():
    form = CreateBlogPostForm()
    return render_template('blog/create_post.html', form=form)

@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    form = CreateBlogPostForm()
    if form.validate_on_submit():
        new_blog = BlogService().create(
            title=form.title.data,
            content=form.content.data,
            uuid=uuid.uuid4().hex
        )
    return redirect(url_for('blog.blogs'))

def __format_str(str):
    str = str.replace('\r','\\r')
    str = str.replace('\n','\\n')
    # str = str.replace('\t','\\t')
    # str = str.replace('"','&quot;')
    # str = str.replace("'", "\\'")

    str = str.replace("'", "\\'")
    return str
