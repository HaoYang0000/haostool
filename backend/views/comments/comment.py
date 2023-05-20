import json
import os
import subprocess
import time
import flask_praetorian
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
import uuid
from backend.services.comments.comment_service import CommentService
from backend.services.users.user_service import UserService
from backend.engine import session_scope
from pypinyin import pinyin, lazy_pinyin, Style
from backend.logs.logger import logger

app = Blueprint(
    'comments',
    __name__,
    url_prefix='/api/comments')
comment_service = CommentService()

# @app.route('/video', methods=['POST'])
# def video_comment():
#     comment_service = CommentService()
#     form = CommentForm()
#     if form.is_submitted():
#         new_comment = comment_service.create(
#             user_id=None if not current_user.is_authenticated else current_user.id,
#             unknown_user_name=form.unknown_user_name.data,
#             content=form.content.data,
#             category='video',
#             video_uuid=form.video_uuid.data
#         )
#         comment = new_comment.serialize
#         if current_user.is_authenticated:
#             user = UserService().get_by_id(current_user.id).serialize
#             comment['user'] = {
#                 'avatar': user.get('avatar')
#             }
#         if new_comment:
#             return comment, 200
#     return 'err', 400


@app.route('/feedback', methods=['GET'])
def get_feedback_comment():
    comments = comment_service.get_all_feedback_comment()
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/video', methods=['GET'])
def get_video_comment():
    comments = comment_service.get_all_video_comment()
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/video/<string:uuid>', methods=['GET'])
def get_video_comment_for_uuid(uuid):
    comments = comment_service.get_reply_for_video_uuid(video_uuid=uuid)
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/blog', methods=['GET'])
def get_blog_comment():
    comments = comment_service.get_all_blog_comment()
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/blog/<string:uuid>', methods=['GET'])
def get_blog_comment_for_uuid(uuid):
    comments = comment_service.get_reply_for_blog_uuid(blog_uuid=uuid)
    return jsonify([comment.serialize for comment in comments]), 200



@app.route('/weeding/table-check', methods=['GET'])
def weeding_table_check_get():
    tables = [
        "刘文炳 刘德成 石秀丽 刘素芬 周兴波 阳运生 刘素荣 李冰 孟凡珍及女儿", #1
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #2
        "王维兴 赵小菊 王乃奇 张明玉 豆豆 小西瓜 郭卫及他姐", #3
        "彭冈及夫人 张淑梅 李振中 耿贵彪 孙如皎家4人 向前", #4
        "李书明及夫人 杨儿子儿媳4人 张兴民及夫人孔和儿子3人 宫姐 姜姐", #5
        "同学家长 孟 王云 石 老郭 杨文娟 李锦萍及老公", #6
        "董禹及父母3人 李建华及老公 李和星及夫人女儿", #7
        "梁爽及办公室同事10人", #8
        "老家阳健仲及朋友 阳健玲及儿子 阳莉萍 肖敏及儿子", #9
        "王铮 王铮女友 陈乾成 孟雨晴 邵威 宋扬 王斌 卫涞 杨松鹤", #10
        "关键 JJ 王炎 美子 段湘森 郑元", #11
        "孟婧 付文阔 赵谭 赵谭男友 唐艺峤 唐艺峤夫人 孙聪 高见闻 王帅 王帅夫人", #12
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #13
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #14
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #15
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #16
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #17
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #18
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #19
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #20
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #21
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #22
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #23
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #24
        "刘祎 李志刚 周易 Eric 王冬梅 刘思琪 王纬及夫人儿子", #25
    ]
    tables_json = []
    for i in range(len(tables)):
        tables_json.append({
            "name": f"{i+1}号桌",
            "people": tables[i],
            "pinyin": "".join([letter[0] for letter in pinyin(tables[i], style=Style.FIRST_LETTER, strict=False)]),
            "pinyin_full": "".join([letter for letter in lazy_pinyin(tables[i], strict=False)])
        })
    return jsonify(tables_json), 200

# @app.route('/blog', methods=['POST'])
# def blog_comment():
#     comment_service = CommentService()
#     comment_service.create(
#         user_id=None if not current_user.is_authenticated else current_user.id,
#         unknown_user_name=request.form['unknown_user_name'],
#         content=request.form['content'],
#         contact_email=request.form['contact_email'],
#         category='blog',
#         blog_uuid=request.form['blog_uuid']
#     )
#     return redirect(f"/blog/view/{request.form['blog_uuid']}")

@app.route('/post-new', methods=['POST'])
def post_new_comment():
    comment_service.create(
        user_id=request.form['user_id'] if 'user_id' in request.form else None,
        unknown_user_name=request.form['name'],
        content=request.form['content'],
        contact_email=request.form['email'] if 'email' in request.form else None,
        category=request.form['category'],
        blog_uuid=request.form['blog_uuid'] if 'blog_uuid' in request.form else None,
        video_uuid=request.form['video_uuid'] if 'video_uuid' in request.form else None,
    )
    return jsonify('success'), 200


@app.route('/deactivate-comment', methods=['POST'])
@flask_praetorian.roles_required(*['root'])
def delete_comment():
    req = request.get_json(force=True)
    result = comment_service.deactive_comment(id=req.get('comment_id'))
    if result:
        return jsonify('success'), 200
    return jsonify('err'), 400
