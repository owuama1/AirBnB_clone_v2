#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This class defines a user by various attributes"""

    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    if storage_type == 'db':
        places = relationship("Place", backref="user",
                              cascade="all, delete-orphan")
    else:
        @property
        def places(self):
            """Getter attribute places that returns the list of Place instances
            with user_id equals to the current User.id"""
            from models import storage
            all_places = storage.all(Place)
            user_places = [place for place in all_places.values()
                           if place.user_id == self.id]
            return user_places
