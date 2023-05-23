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
        "刘文炳 刘德成 石秀丽 刘素芬 周兴波 阳运生 刘素荣 李冰 孟凡珍及家人", #1
        "吴昌进 杨举田 杨云田 王安怀 杨善臻 吴昌元 赵同芳", #2
        "刘祎 李正纲 周易 Eric 王冬梅 刘思琪 王纬及家人", #3
        "聂瑞明及家人 邱根来及家人 李斌及家人 李涛及家人", #4
        "王维兴 赵小菊 王乃奇 张明玉及家人 郭卫 郭建 王俊涛 田威", #5
        "王兆成 白云飞 李岳及家人 马永 戚建民", #6
        "彭冈及家人 张淑梅 李振中 耿贵彪 孙如皎 王宜青及家人 向前", #7
        "王复升及家人 于瑞国及家人 于新才及家人 刘卫东及家人 洪晓英及家人", #8
        "李书明及家人 李晨及家人 张兴民 孔祥荣 姜力 宫玉芳", #9
        "刘纪坤及家人 曹乃刚 冯业水 葛景中 姜化勇 陈昌伦及家人", #10
        "孟宪茹 王云 石振伟 郭耀敏 杨文娟 李锦萍 李琛 赵朝霞 刘勇", #11
        "赵明月及家人 郑翔文 高庆峰及家人 吴奎强 张玉凤 吴磊", #12
        "宋兰启 董自强 董宇 李建华 何万通 李和星 程铭 李米 赵朝霞 刘勇", #13
        "李长丽及家人 杜艳明及家人 王绍君 仇丽丽及家人 张娜", #14
        "谭盛凛 邢钰 王芳 阎培林 李刚 刘振 梁爽 王强 田静", #15
        "夏淑华及家人 李玉梅及家人 李颖及家人 李红霞", #16
        "白雨萌 陈鑫 胡佳 梁晨 孔琳 张鑫 孔小兴 陈峰", #17
        "阳健仲及朋友 阳健玲及家人 阳莉萍 肖敏及家人", #18
        "韩云峰 胡月龙 耿一鹤 毕波 郑健 韩硕 贾萌", #19
        "关键 王炎 李美慧 段湘森 郑元 邵威 孟婧 付文阔 赵谭 张龙飞", #20
        "唐艺峤 孙聪 高见闻 王帅 赵洪飞 柳萌 贾荟媛 房江 张懿斐 申薇", #21
        "张钰暄 翟浩 张舵 任乐乐 于文静 赵安然 田云绯 于筱萱", #22
        "王铮 俞蔚然 陈乾成 孟雨晴 宋扬 王斌 卫涞 杨松鹤", #23
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
