import logging
from datetime import datetime, timedelta
from typing import List
from main import db
from models.notifications import NotificationModel
from models.frequencies import RecurringFrequencyModel
from models.types import NotificationTypeModel
from services.base import BaseService
from sqlalchemy import desc, or_
from libs.constants import MAX_DELAY_TIME

logger = logging.getLogger('flask.app')


class NotificationService(BaseService):
    model = NotificationModel

    def get_all(self, **kwargs):
        """
        Return api list result

        Returns:
            model
        """

        query = self.model.query.filter(self.model.active == 1)

        if kwargs.get('user_id') is not None:
            query = query.filter(self.model.user_id == kwargs.get('user_id'))

        query = query.order_by(desc(self.model.id))
        query = self.paginate(query, kwargs)

        return query.all()

    def get_by_id(self, notification_id, **kwargs):
        """
        Return api detail result

        Args:
            notification_id (int): primary key

        Returns:
            model | null
        """
        return self.model.query.filter(self.model.id == notification_id, self.model.active == 1).one_or_none()

    def delete_by_id(self, notification_id, **kwargs):
        """
        Delete a record by id

        Args:
            notification_id (int): primary key

        Returns:
            bool
        """
        record = self.get_by_id(notification_id)

        if record is None:
            logger.debug('Deleting {model_name} failed with id: {id}, record not found'.format(
                model_name=self.model.__table__.name,
                id=notification_id
            ))
            return False
        else:
            record.active = 0
            db.session.commit()
            logger.debug('Deleting {model_name} from {data}'.format(
                data=record,
                model_name=self.model.__table__.name
            ))
            return True

    def get_unsent_notifications(self):
        """
        :return:
        """
        now = datetime.now()
        until_time = now + timedelta(
            seconds=MAX_DELAY_TIME
        )

        notifications: List[NotificationModel] = db.session\
            .query(NotificationModel)\
            .filter(NotificationModel.active == True)\
            .filter(NotificationModel.start_at < until_time)\
            .filter(
                or_(
                    NotificationModel.send_at == None,
                    NotificationModel.send_at <= now
                )
            ).all()

        return notifications

    def validate_foreign_key(self, **kwargs):
        """
            Check if a recurring_frequency_id, notification_type_id exists before creating a notification
        """
        result_type = NotificationTypeModel.query.filter(NotificationTypeModel.id == kwargs.get('notification_type_id', None)).one_or_none()
        result_frequency = RecurringFrequencyModel.query.filter(RecurringFrequencyModel.id == kwargs.get('recurring_frequency_id', None)).one_or_none()

        if result_type is None or result_frequency is None:
            return False

        return True
