import logging

from app.schemas.logs import NotificationLogSchema
from app.services.logs import LogService
from flask import Blueprint, abort, make_response
from flask_api import status
from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from libs.schema_tool import unrequire

logger = logging.getLogger('flask.app')

app = Blueprint(
    'logs',
    __name__,
    url_prefix='/logs'
)

@doc(tags=['Notification logs'])
class LogsList(MethodResource):
    log_service = LogService()

    @marshal_with(NotificationLogSchema(many=True), code=status.HTTP_200_OK)
    @doc(description='return all logs')
    def get(self, **kwargs):
        return self.log_service.get_all(), status.HTTP_200_OK

    @use_kwargs(NotificationLogSchema().fields)
    @marshal_with(NotificationLogSchema, code=status.HTTP_201_CREATED)
    @doc(description='Create a log')
    def post(self, **kwargs):
        validation = self.log_service.validate_foreign_key(**kwargs)
        if validation is False:
            abort(status.HTTP_400_BAD_REQUEST)
        new_log = self.log_service.create(**kwargs)
        return new_log, status.HTTP_201_CREATED

@doc(tags=['Notification logs'])
class LogsDetail(MethodResource):
    log_service = LogService()

    @marshal_with(NotificationLogSchema, code=status.HTTP_200_OK)
    @doc(description='return a log with id')
    def get(self, log_id, **kwargs):
        result = self.log_service.get_by_id(log_id)
        if result == None:
            abort(status.HTTP_404_NOT_FOUND)
        return result, status.HTTP_200_OK
    
    @marshal_with(None, code=status.HTTP_204_NO_CONTENT)
    @doc(description='delete a log with id')
    def delete(self, log_id, **kwargs):
        response = self.log_service.delete_by_id(log_id)
        if response == False:
            abort(status.HTTP_404_NOT_FOUND)
        return make_response('', status.HTTP_204_NO_CONTENT)
    
    @use_kwargs(NotificationLogSchema().fields)
    @marshal_with(NotificationLogSchema, code=status.HTTP_200_OK)
    @doc(description='update a log with id with full record')
    def put(self, log_id, **kwargs):
        result = self.log_service.update_by_id(log_id, kwargs)
        if result == None:
            abort(status.HTTP_404_NOT_FOUND)
        return result, status.HTTP_200_OK

    @use_kwargs(unrequire(NotificationLogSchema().fields))
    @doc(description='partially update a log')
    @marshal_with(NotificationLogSchema, code=status.HTTP_200_OK)
    def patch(self, log_id, **kwargs):
        result = self.log_service.update_by_id(log_id, kwargs)
        if result == None:
            abort(status.HTTP_404_NOT_FOUND)
        return result, status.HTTP_200_OK

app.add_url_rule(
    '',
    view_func=LogsList.as_view('LogsList'),
    methods=['GET', 'POST']
)
app.add_url_rule(
    '/<int:log_id>',
    view_func=LogsDetail.as_view('LogsDetail'),
    methods=['GET', 'PUT', 'DELETE', 'PATCH']
)
