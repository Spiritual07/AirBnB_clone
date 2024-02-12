#!/usr/bin/python3
"""Module for Amenity class"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class that inherit from BaseModel
    Attributes:
        name (str): The name of the amenit
    """

    name = ""
