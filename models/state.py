#!/usr/bin/python3
"""This is the state class """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
from os import environ


class State(BaseModel, Base):
    """class for state
    Attributes:
        name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City",
                          backref="state",
                          cascade="all, delete-orphan",
                          passive_deletes=True)

    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            return [city for city in models.storage.all(
                City).values() if city.state_id == self.id]
