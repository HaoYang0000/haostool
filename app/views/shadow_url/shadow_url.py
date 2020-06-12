import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
from flask_socketio import SocketIO, send, emit
from app.engine import db, socketIO
from flask_login import login_required

import uuid

app = Blueprint(
    'shadow_url',
    __name__,
    url_prefix='/shadow_url'
)
logger = logging.getLogger(__name__)


@app.route('/show_secret_service', methods=['POST'])
@login_required
def shadow_url():
    data = request.form['token']

    # verify token
    url = url_for('index.special')
    result = {}
    result['href'] = '<a class="nav-button right-align" href="#" onclick="test()">特殊内容</a>'
    result['code'] = 'function test(){alert(1);}'

    generated_tag = '<a class="nav-button right-align" href="#" onclick="test()">特殊内容</a><script type="text/javascript"></script>'
    return jsonify(result)

@app.route('/get_functions', methods=['POST'])
def get_functions():
    if current_user.is_authenticated:
        csrf_token = request.form['csrf_token']

        result = {}
        result['code'] = 'function fire_it_up(token){$.ajax({type:"POST",data:{token:token},url:"/shadow_url/show_secret_service",dataType:"json",success:function(data){document.getElementById("secretnav").style.display="block";document.getElementById("secretnav").innerHTML=data.href},error:function(jqXHR){console.log(jqXHR)}})}var counter_left=0;var counter_right=0;var nav_button=document.getElementById("nav_setting_button");document.getElementById("nav_setting_button").addEventListener("mouseover",function(){counter_left++;if(counter_right===5&&counter_left===5){fire_it_up(123)}});var logout_button=document.getElementById("logout_button");document.getElementById("logout_button").addEventListener("mouseover",function(){counter_right++;if(counter_right===5&&counter_left===5){fire_it_up(123)}});'
        # function fire_it_up(token) {
        #         $.ajax({
        #             type: "POST",
        #             data:{
        #                 token:token
        #             },
        #             url: "/shadow_url/show_secret_service",
        #             dataType: "json",
        #             success: function(data) { 
        #                 document.getElementById("secretnav").style.display = "block";
        #                 document.getElementById("secretnav").innerHTML = data.href;  
        #             },
        #             error: function(jqXHR) {
        #                 console.log(jqXHR);
        #             }
        #         })
        #     }
        # var counter_left = 0;
        #     var counter_right = 0;
        #     var nav_button = document.getElementById("nav_setting_button");
        #     document.getElementById("nav_setting_button").addEventListener("mouseover", function() {
        #         counter_left++;
        #         if (counter_right === 5 && counter_left === 5) {
        #             fire_it_up(123);
        #         }
        #     });
        #     var logout_button = document.getElementById("logout_button");
        #     document.getElementById("logout_button").addEventListener("mouseover", function() {
        #         counter_right++;
        #         if (counter_right === 5 && counter_left === 5) {
        #             fire_it_up(123);
        #         }
        #     });
        
        return jsonify(result)
    else:
        return 'error', 401
    