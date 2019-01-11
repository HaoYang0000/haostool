from flask import abort
from flask_api import status
from sqlalchemy import inspect, exists
from sqlalchemy.orm import joinedload, lazyload, Query
from sqlalchemy import inspect, exists, func
import logging
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

logger = logging.getLogger('flask.app')


class BaseService:
    model = None

    def __init__(self):
        """
        Check if model is set up properly in the child service

        Raises:
            Exception
        """
        if self.model is None:
            raise Exception(
                "{class_name} missing model attribute".format(
                    class_name=self.__class__.__name__
                )
            )

    def get_all(self, **kwargs):
        """
        Return api list result

        Returns:
            model | null
        """
        return self.model.query.filter_by(**kwargs).all()
    
    def get_by_id(self, id, **kwargs):
        """
        Return api detail result

        Args:
            param1 (int): primary key

        Returns:
            model | null
        """
        return self.model.query.filter(self.model.id == id).one_or_none()

    def create(self, **kwargs):
        """
        Add new model record

        Returns:
            model
        """
        new_model = self.model(**kwargs)
        db.session.add(new_model)
        db.session.commit()
        logger.debug('Creating new item {model_name} with {data}'.format(data=new_model, model_name=self.model.__table__.name))
        return new_model

    def delete_by_id(self, id, **kwargs):
        """
        Delete a record by id

        Args:
            param1 (int): primary key

        Returns:
            bool
        """
        record = self.get_by_id(id)

        if record == None:
            logger.debug('Deleting {model_name} failed with id: {id}, record not found'.format(model_name=self.model.__table__.name, id=id))
            return False
        else:
            db.session.delete(record)
            db.session.commit()
            logger.debug('Deleting {model_name} from {data}'.format(data=record, model_name=self.model.__table__.name))
            return True

    def update_by_id(self, id, data):
        """
        Update a record by id

        Args:
            param1 (int): primary key
        
        Returns:
            model | null
        """
        record = self.model.query.filter(self.model.id == id)

        if record.one_or_none() == None:
            logger.debug('Updating {model_name} failed with id: {id}, record not found'.format(model_name=self.model.__table__.name, id=id))
            return None
        else:
            record.update(data)
            db.session.commit()
            logger.debug('Updating {model_name} with {data}, id:{id}'.format(
                data=data,
                model_name=self.model.__table__.name,
                id=id)
            )
            return record.first()

    def paginate(self, query, kwargs):
        limit = kwargs.get('limit', 10)
        limit = limit if limit > 0 else 10

        page = kwargs.get('page', 1)
        page = page if page > 0 else 1

        offset = (page - 1) * limit

        return query.limit(limit).offset(offset)
