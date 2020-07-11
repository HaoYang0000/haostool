from app.services.user.user_service import UserService
from functools import wraps
from flask import abort
from flask_login import current_user
from app.engine import ALLOWED_EXTENSIONS
from os.path import isfile, join
from os import listdir
from mimetypes import MimeTypes
import hashlib
import json
import time
import hmac
import copy
import sys
import os

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user:
            print(current_user.id)
            if UserService().is_admin(user_id=current_user.id):
                return func(*args, **kwargs)
        else:
            abort(401)
        abort(403)
    return wrapper

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def merge_dicts(a, b, path = None):
    """
    Deep merge two dicts without modifying them. Source: http://stackoverflow.com/questions/7204805/dictionaries-of-dictionaries-merge/7205107#7205107
    Parameters:
        a: dict
        b: dict
        path: list
    Return:
        dict: Deep merged dict.
    """
    aClone = copy.deepcopy(a);
    # Returns deep b into a without affecting the sources.
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                aClone[key] = merge_dicts(a[key], b[key], path + [str(key)])
            else:
                aClone[key] = b[key]
        else:
            aClone[key] = b[key]
    return aClone

def calc_hmac(key, string, hex = False):
    """
    Calculate hmac.
    Parameters:
        key: string
        string: string
        hex: boolean optional, return in hex, else return in binary
    Return:
        string: hmax in hex or binary
    """

    # python 2-3 compatible:
    try:
        hmac256 = hmac.new(key.encode() if isinstance(key, str) else key, msg = string.encode("utf-8") if isinstance(string, str) else string, digestmod = hashlib.sha256) # v3
    except Exception:
        hmac256 = hmac.new(key, msg = string, digestmod = hashlib.sha256) # v2

    return hmac256.hexdigest() if hex else hmac256.digest()

