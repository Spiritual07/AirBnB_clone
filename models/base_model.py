#!/usr/bin/python3
"""Defines the BaseModel class."""

import uuid
from datetime import datetime
import models


class BaseModel():
    """Represents the BaseModel of the HBnB project."""
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""

        TimeFormat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "create_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, TimeFormat))
                else:
                    setattr(self, key, value)

        models.storage.new(self)

    def save(self):
        """updates the public instance attribute updated_at with
        the current datetime
        """

        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of
        __dict__ of the instance
        """

        i_dict = self.__dict__.copy()
        i_dict["__class__"] = self.__class__.__name__
        if isinstance(i_dict["created_at"], str):
            i_dict["created_at"] = datetime.fromisoformat(i_dict["created_at"])
        if isinstance(i_dict["updated_at"], str):
            i_dict["updated_at"] = datetime.fromisoformat(i_dict["updated_at"])
        i_dict["created_at"] = i_dict["created_at"].isoformat()
        i_dict["updated_at"] = i_dict["updated_at"].isoformat()

        return i_dict

    def __str__(self):
        """String representation of the class"""

        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
