from typing import Any


def add_dictionary_support(class_in: Any) -> Any:
    """
    Adds the support to get the attributes using the dict() command to any class.

    Meant to be used as a decorator.
    :param class_in: The class to which the support should be added
    :return:
    """
    class_out = class_in

    def __iter__(self):
        self._dict_iteration = 0
        return self

    def __next__(self):
        all_attributes = self.__dict__.copy()
        all_attributes.pop("_dict_iteration")
        if self._dict_iteration < len(all_attributes):
            next_element = list(all_attributes.items())[self._dict_iteration]
            self._dict_iteration += 1
            return next_element
        else:
            raise StopIteration

    class_out.__iter__ = __iter__
    class_out.__next__ = __next__
    return class_out
