#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import os

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """ Serializes instances to a JSON file & deserializes back to instances """

    # string - path to the JSON file
    __file_path = os.path.relpath("file.json")
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file (path: __file_path) """
        json_objects = {}
        for key, obj in self.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """ Deserializes the JSON file to __objects """
        try:
            with open(self.__file_path, 'r') as f:
                jo = dict(json.load(f))
            for key, dic in jo.items():
                self.__objects[key] = classes[dic.get("__class__")](**dic)
        except BaseException:
            pass

    def delete(self, obj=None):
        """ Delete obj from __objects if it's inside """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """ Call reload() method for deserializing the JSON file to objects """
        self.reload()

    def get(self, cls, id):
        """ Retrieves one object from storage """
        for o in self.__objects.values():
            if o.__class__ == cls or o.__class__.__name__ == cls\
                    and o.id == id:
                return o

    def count(self, cls=None):
        """ Count the number of objects in storage """
        if cls is not None:
            counter = 0
            for o in self.__objects.values():
                if o.__class__ == cls or o.__class__.__name__ == cls:
                    counter += 1
            return counter
        return len(self.__objects.keys())
