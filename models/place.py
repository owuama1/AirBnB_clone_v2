#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Table, Column, String, ForeignKey
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy.orm import relationship

class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", cascade="all, delete", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    else:
        @property
        def reviews(self):
            """ Getter attribute that returns the list of Review instances """
            from models import storage
            review_list = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """ Getter attribute that returns the list of Amenity instances """
            from models import storage
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = storage.get(Amenity, amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """ Setter attribute that appends an Amenity instance to amenity_ids """
            if isinstance(obj, Amenity):
                if self.id:
                    self.amenity_ids.append(obj.id)

    city_id = Column(String(60), nullable=False)
    user_id = Column(String(60), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))
