import json

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response
from flask_api import status
from flask_login import current_user, login_user, logout_user
from backend.services.aws.aws_service import AwsService
from flask import send_from_directory
from collections import namedtuple
import flask_praetorian
from backend.logs.logger import logger

VpnInstance = namedtuple(
    "VpnInstance", ['name', 'type', 'state', 'ip_address'])

app = Blueprint('aws', __name__, url_prefix='/api')
aws_service = AwsService()
aws_service._init_connect()


@app.route('/aws', methods=['GET'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def aws():
    instance_list = aws_service.list_instances()
    vpn_instance = instance_list.get('Reservations')[0].get('Instances')[0]
    instance = VpnInstance(
        name=vpn_instance.get('Tags')[0].get('Value'),
        type=vpn_instance.get('InstanceType'),
        state=vpn_instance.get('State').get('Name'),
        ip_address=vpn_instance.get('PublicIpAddress')
    )
    return jsonify(instance._asdict()), 200


@app.route('/aws/start_instance', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def aws_start_instance():
    response = aws_service.start_instance()
    return jsonify("success"), 200


@app.route('/aws/stop_instance', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def aws_stop_instance():
    response = aws_service.stop_instance()
    return jsonify("success"), 200


@app.route('/aws/change_ip', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def aws_change_vpn_ip():
    response = aws_service.replace_elastic_address()
    return jsonify("success"), 200


@app.route('/aws/remote/start-instance/<string:device>/<string:token>', methods=['GET'])
def aws_remote_start_instance(device, token):
    logger.info(f"Starting VPN from device: {device} with token: {token}")

    if not device or token != 'test':
        return jsonify("Bad input"), 400

    response = aws_service.start_instance()
    return jsonify("success"), 200


@app.route('/aws/remote/stop-instance/<string:device>/<string:token>', methods=['GET'])
def aws_remote_stop_instance(device, token):
    logger.info(f"Stopping VPN from device: {device} with token: {token}")

    if not device or token != 'test':
        return jsonify("Bad input"), 400

    response = aws_service.stop_instance()
    return jsonify("success"), 200
