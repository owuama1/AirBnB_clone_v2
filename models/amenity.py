#!/usr/bin/python3
""" Amenity Module for HBNB project """
from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.place import place_amenity

class Amenity(BaseModel, Base):
    """ Amenity class to store amenity information """

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    place_amenities = relationship(
        'Place',
        secondary=place_amenity,
        backref='amenities',
        viewonly=False
    )
