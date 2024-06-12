#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from models import storage  # Import storage here

        if storage_type == 'db':
            self.cities = relationship("City", backref="state", cascade="all, delete-orphan")
        else:
            @property
            def cities(self):
                """Getter attribute cities that returns the list of City instances
                with state_id equals to the current State.id"""
                all_cities = storage.all(City)
                state_cities = [city for city in all_cities.values()
                                if city.state_id == self.id]
                return state_cities
