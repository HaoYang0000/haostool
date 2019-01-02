import logging

from marshmallow import fields
from app.schemas.notifications import NotificationSchema
from app.services.notifications import NotificationService
from flask import Blueprint, abort, make_response
from flask_api import status
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from libs.schema_tool import unrequire
from daemon.helpers.publisher import DaemonPublisher

logger = logging.getLogger('flask.app')

app = Blueprint(
    'notifications',
    __name__,
    url_prefix='/notifications'
)

@doc(tags=['Notifications'])
class NotificationsList(MethodResource):
    notification_service = NotificationService()


    @use_kwargs({'user_id': fields.Int(), 'limit': fields.Int(), 'page': fields.Int()})
    @marshal_with(NotificationSchema(many=True), code=status.HTTP_200_OK)
    @doc(description='return all notifications')
    def get(self, **kwargs):
        return self.notification_service.get_all(**kwargs), status.HTTP_200_OK


    @use_kwargs(NotificationSchema().fields)
    @marshal_with(NotificationSchema, code=status.HTTP_201_CREATED)
    @doc(description='Create a notification')
    def post(self, **kwargs):
        validation = self.notification_service.validate_foreign_key(**kwargs)
        if validation == False:
            abort(status.HTTP_400_BAD_REQUEST)
        notification = self.notification_service.create(**kwargs)
        notification_protobuf = notification.get_protobuf()
        publisher = DaemonPublisher()

        try:
            publisher.publish(notification_protobuf)
        except Exception:
            # Try again
            try:
                publisher.publish(notification_protobuf)
            except Exception as e:
                logging.exception(str(e))

        return notification, status.HTTP_201_CREATED

@doc(tags=['Notifications'])
class NotificationsDetail(MethodResource):
    notification_service = NotificationService()

    @marshal_with(NotificationSchema, code=status.HTTP_200_OK)
    @doc(description='return a notification with id')
    def get(self, notification_id, **kwargs):
        result = self.notification_service.get_by_id(notification_id)
        if result == None:
            abort(status.HTTP_404_NOT_FOUND)
        return result, status.HTTP_200_OK
    
    @marshal_with(None, code=status.HTTP_204_NO_CONTENT)
    @doc(description='delete a notification with id')
    def delete(self, notification_id, **kwargs):
        response = self.notification_service.delete_by_id(notification_id)
        if response == False:
            abort(status.HTTP_404_NOT_FOUND)
        return make_response('', status.HTTP_204_NO_CONTENT)
    
    @use_kwargs(NotificationSchema().fields)
    @marshal_with(NotificationSchema, code=status.HTTP_200_OK)
    @doc(description='update a notification with id with full record')
    def put(self, notification_id, **kwargs):
        result = self.notification_service.update_by_id(notification_id, kwargs)
        if result == None:
            abort(status.HTTP_404_NOT_FOUND)
        return result, status.HTTP_200_OK

    @use_kwargs(unrequire(NotificationSchema().fields))
    @doc(description='partially update a notification')
    @marshal_with(NotificationSchema, code=status.HTTP_200_OK)
    def patch(self, notification_id, **kwargs):
        result = self.notification_service.update_by_id(notification_id, kwargs)
        if result == None:
            abort(status.HTTP_404_NOT_FOUND)
        return result, status.HTTP_200_OK

app.add_url_rule(
    '',
    view_func=NotificationsList.as_view('NotificationsList'),
    methods=['GET', 'POST']
)
app.add_url_rule(
    '/<int:notification_id>',
    view_func=NotificationsDetail.as_view('NotificationsDetail'),
    methods=['GET', 'PUT', 'DELETE', 'PATCH']
)