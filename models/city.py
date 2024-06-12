#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """ The city class, contains state ID and name """

    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    if storage_type == 'db':
        places = relationship("Place", backref="city",
                              cascade="all, delete-orphan")
    else:
        @property
        def places(self):
            """Getter attribute places that returns the list of Place instances
            with city_id equals to the current City.id"""
            from models import storage
            all_places = storage.all(Place)
            city_places = [place for place in all_places.values()
                           if place.city_id == self.id]
            return city_places
