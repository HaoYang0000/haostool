from backend.engine import ALLOWED_EXTENSIONS


def allowed_profile_img_format(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
