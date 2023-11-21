#!/usr/bin/python3
"""
New engine DBStorage
"""
import os
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


class DBStorage():
    """DB Storage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialization of Engine"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}".
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST'),
                                             os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        res = {}
        if cls is None:
            obj = [User, State, City, Amenity, Place, Review]
        else:
            obj = self.__session.query(cls).all()
        for i in obj:
            k = f"{i.__class__.__name__}.{i.id}"
            res[k] = i
        return res

    def new(self, obj):
        """Add the object to DB"""
        self.__session.add(obj)

    def save(self):
        """commit all cham=nge of the DB"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        drop and recreate all tables in the database"""
        Base.metadata.create_all(bind=self.__engine)
        new_session = scoped_session(sessionmaker(expire_on_commit=False,
                                     bind=self.__engine))
        self.__session = new_session

    def close(self):
        """ close opened sessions for private session """
        self.__session.remove()
