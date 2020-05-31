import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, send_from_directory
from flask_api import status
from flask_login import current_user, login_user, logout_user
from app.controllers.main_controller import MainController as Controller
from app.forms.slack_emoji.slack_emoji_form import SlackEmojiForm
from app.services.slack_emoji.run import generate
from flask import send_from_directory


UPLOAD_FOLDER = '/app/uploads/'
app = Blueprint('index', __name__)
logger = logging.getLogger(__name__)

controller = Controller(current_user=current_user)


@app.route('/health', methods=['GET', 'POST'])
def health():
    return 'OK', status.HTTP_201_CREATED


@app.route('/', methods=['GET', 'POST'])
def main():
    logger.error(request.headers.get('Accept-Language', ''))
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        all_service = controller.get_all_service()
        return render_template('index.html', current_user=current_user, all_service=all_service)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/donate', methods=['GET', 'POST'])
def donate_page():
    return render_template('donate.html')


@app.route('/comment', methods=['GET', 'POST'])
def comment_page():
    return render_template('comment.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_us():
    return render_template('contact.html')

@app.route('/special', methods=['GET', 'POST'])
def special():
    return render_template('special.html')

@app.route('/slack_emoji', methods=['GET', 'POST'])
def slack_emoji():
    form = SlackEmojiForm()
    output = ''
    if form.validate_on_submit():
        output = generate(emoji=form.emoji.data, padding=form.padding.data, input=form.input.data,
                          if_reverse=form.if_reverse.data, if_same_line=form.if_same_line.data,
                          if_copy_to_clipboard=False)
        logger.error(output)
    return render_template('slack_emoji.html', form=form, output=output)


@app.route('/kglb/<whatever>/<int:times>', methods=['GET', 'POST'])
def lol(whatever, times):
    return_list = []
    for x in range(times):
        return_list.append(whatever)
    return render_template('whatever.html', whatever=return_list)


@app.errorhandler(401)
def login_required(e):
    # note that we set the 404 status explicitly
    return redirect(url_for('auth.login')), 401


@app.errorhandler(Exception)
def exception_handler(error):
    return "!!!!" + repr(error)
