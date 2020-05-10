import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response
from flask_api import status
from flask_login import current_user, login_user, logout_user
from app.controllers.main_controller import MainController as Controller
from app.services.aws.aws_service import AwsService
from flask import send_from_directory
from collections import namedtuple
from flask_login import login_required

VpnInstance=namedtuple("VpnInstance",['name','type','state', 'ip_address'])

app = Blueprint('aws', __name__)
logger = logging.getLogger(__name__)


@app.route('/aws', methods=['GET', 'POST'])
def aws():
    aws_service = AwsService()
    aws_service._init_connect()
    instance_list = aws_service.list_instances()
    logger.error(instance_list)
    vpn_instance = instance_list.get('Reservations')[0].get('Instances')[0]
    instance = VpnInstance(
        name=vpn_instance.get('Tags')[0].get('Value'),
        type=vpn_instance.get('InstanceType'),
        state=vpn_instance.get('State').get('Name'),
        ip_address=vpn_instance.get('PublicIpAddress')
    )
    return render_template('aws/aws.html', vpn_instance=instance)

@app.route('/aws/start_instance', methods=['POST'])
@login_required
def aws_start_instance():
    aws_service = AwsService()
    aws_service._init_connect()
    response = aws_service.start_instance()
    return jsonify(response)

@app.route('/aws/stop_instance', methods=['POST'])
@login_required
def aws_stop_instance():
    aws_service = AwsService()
    aws_service._init_connect()
    response = aws_service.stop_instance()
    return jsonify(response)

@app.route('/aws/change_ip', methods=['POST'])
@login_required
def aws_change_vpn_ip():
    aws_service = AwsService()
    aws_service._init_connect()
    response = aws_service.replace_elastic_address()
    return jsonify(response)