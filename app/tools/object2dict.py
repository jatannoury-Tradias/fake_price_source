from typing import Any
from decimal import Decimal

json_types = [str, Decimal, int, bool]


def object2dict(object_in: Any):
    if isinstance(object_in, list):
        return [object2dict(value) for value in object_in]
    elif isinstance(object_in, float):
        return Decimal(object_in)
    elif isinstance(object_in, dict):
        return {key: object2dict(value) for key, value in object_in.items()}
    elif object_in is None:
        return object_in
    elif any([isinstance(object_in, data_type) for data_type in json_types]):
        return object_in
    elif isinstance(object_in, object):
        out_dict = {}
        for key, value in object_in.__dict__.items():
            if any([isinstance(value, data_type) for data_type in json_types]):
                out_dict[key] = value
            else:
                out_dict[key] = object2dict(value)
        return out_dict
    else:
        return object_in