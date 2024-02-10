#!/usr/bin/python3

import os
from models.base_model import BaseModel
import json
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Method that returns the dictionary __objects"""

        return FileStorage.__objects
    
    def new(self, obj):
        """Method That sets in __objects the obj with key <obj class name>.id"""

        ObjClassName = obj.__class__.__name__
        key = "{}.{}".format(ObjClassName, obj.id)
        FileStorage.__objects[key] = obj
    
    def save(self):
        """Method that serializes __objects to the JSON file (path: __file_path)"""

        total_obj = FileStorage.__objects
        ObjDict = {}
        for obj in total_obj.keys():
            ObjDict[obj] = total_obj[obj].to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(ObjDict, f)
    
    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file (__file_path) exists
         otherwise, do nothing. If the file doesn’t exist, no exception should be raised)
        """
        
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                try:
                    ObjDict = json.load(f)
                    for key, value in ObjDict.items():
                        class_name, obj_id = key.split('.')

                        cls = eval(class_name)
                        instance = cls(**value)
                        FileStorage.__objects[key] = instance
                except Exception:
                    pass
