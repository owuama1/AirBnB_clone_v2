#!/usr/bin/python3
""" City Module for HBNB project """
import os
from sqlalchemy import Column, String, ForeignKey, relationship  # Add relationship import
from models.base_model import BaseModel, Base

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        from models.place import Place
        places = relationship("Place", backref="city", cascade="all, delete")
