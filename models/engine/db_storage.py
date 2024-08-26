#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in a database"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        classes = [User, State, City, Amenity, Place, Review]
        new_dict = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            for key, value in self.__session.query(cls).all():
                new_dict[key] = value
        else:
            for c in classes:
                for key, value in self.__session.query(c).all():
                    new_dict[key] = value
        return new_dict

    def new(self, obj):
        """Adds new object to storage"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the current session"""
        self.__session.close()

    def get(self, cls, id):
        """Returns the object based on the class name and its ID, or None"""
        if cls and id:
            return self.__session.query(eval(cls)).get(id)
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage
        matching the given class name
        """
        if cls:
            return len(self.all(cls))
        return len(self.all())
