#!/usr/bin/python3
"""Module for class state"""

from models.base_model import BaseModel


class State(BaseModel):
    """State class that inherit from BaseModel
    Attributes:
        name (str): The name of the state
    """

    name = ""
