#!/usr/bin/python3
"""Module for class City"""

from models.base_model import BaseModel

class City(BaseModel):
    """City class that inherit from BaseModel
    Attributes:
        state_id (str): The state id.
        name (str): The name of the city.
    """

    state_id = ""
    name = ""