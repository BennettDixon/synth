#!/usr/bin/python3
"""
Contains class BaseModel
"""

from os import getenv
import uuid


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                         self.to_dict())

    def update(self, ignore, *args, **kwargs):
        """updates the instance using a dictionary of kwargs"""
        for k, v in kwargs.items():
            if k in ignore:
                continue
            setattr(self, k, v)

    def to_dict(self, save_pass=False):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        new_dict = self.prettify(new_dict)
        return new_dict

    @classmethod
    def prettify(cls, my_dict):
        """
        Removes the name mangling caused by private
        instance attributes by removing the class name
        and the 3 underscores
        """
        my_items = my_dict.copy()
        for key in my_items.keys():
            if '_{}__'.format(my_dict["__class__"]) in key:
                mangled = len(my_dict["__class__"]) + 3
                new_key = key[mangled:]
                my_dict[new_key] = my_items[key]
                del my_dict[key]
        return my_dict
