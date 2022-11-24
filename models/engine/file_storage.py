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
<<<<<<< HEAD
    """Performs serialization and deserialization of object."""
=======
    """ Serializes instances to a JSON file & deserializes
        back to instances
    """
>>>>>>> nick

    # string - path to the JSON file
    __file_path = os.path.relpath("file.json")
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects """
        if cls is not None:
            new_dict = {}
            for key, value in FileStorage.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return FileStorage.__objects

    def new(self, obj):
        """ Sets in __objects the obj with key <obj class name>.id """
        if obj is not None:
<<<<<<< HEAD
            key = obj.__class__.__name__ + "." + obj.id
=======
            key = f"{obj.__class__.__name__}.{obj.id}"
>>>>>>> nick
            FileStorage.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file (path: __file_path) """
        json_objects = {}
<<<<<<< HEAD
        for key in FileStorage.__objects:
            json_objects[key] = FileStorage.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
=======
        for key, obj in FileStorage.__objects.items():
            json_objects[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
>>>>>>> nick
            json.dump(json_objects, f)

    def reload(self):
        """ Deserializes the JSON file to __objects """
        try:
<<<<<<< HEAD
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                objects = json.load(f)
        except FileNotFoundError:
=======
            with open(FileStorage.__file_path, 'r') as f:
                jo = dict(json.load(f))
            for key, dic in jo.items():
                FileStorage.__objects[key] = classes[dic.get(
                    "__class__")](**dic)
        except BaseException:
>>>>>>> nick
            pass
        else:
            for obj in objects.values():
                self.new(eval(obj.get('__class__'))(**obj))

    def delete(self, obj=None):
        """ Delete obj from __objects if it's inside """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
<<<<<<< HEAD

    def get(self, cls, id):
        """Retrieve an object from the file storage.

        The object retrieved is based on the `class` and `id`
        or None if not found.
        Args:
            cls (class): The class of the object to be retrieved.
            id (string): String representing the object id.
        Return:
            object or None.
        """
        key = "%s.%s" % (classes.get(cls.__name__).__name__, id)
        return FileStorage.__objects.get(key)
=======

    def close(self):
        """ Call reload() method for deserializing the JSON file to objects """
        self.reload()

    def get(self, cls, id):
        """ Retrieves one object from storage """
        for o in FileStorage.__objects.values():
            if o.__class__ == cls or o.__class__.__name__ == cls\
                    and o.id == id:
                return o
>>>>>>> nick

    def count(self, cls=None):
        """Count the number of objects in storage.

        Counts the number of objects in storage matching the given
        class. If no class is passed as an argument, count all the
        objects in storage.
        Args:
            cls (class): class of the objects of interest.
        Returns:
            Total number of objects in storage(overall or of a
            particular class).
        """
        if cls is not None:
<<<<<<< HEAD
            count = 0
            for obj in FileStorage.__objects.values():
                if obj.__class__ == cls or\
                        obj.__class__.__name__ == cls:
                            count += 1
            return count
        return len(self.all())

    def close(self):
        """deseserialize JSON file."""
        self.reload()
=======
            counter = 0
            for o in FileStorage.__objects.values():
                if o.__class__ == cls or o.__class__.__name__ == cls:
                    counter += 1
            return counter
        return len(FileStorage.__objects.keys())
>>>>>>> nick
