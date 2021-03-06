import datetime
from rest_framework.utils import json
from collectionapp.models import Collection


def validate_item_fields(data):
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, str):
                raise TypeError('names of fields can be strings only')
    else:
        raise TypeError('fields must be included in a list')


def validate_fields_from_request_to_fields_in_collection(collection, data):
    item_text_fields = json.loads(collection.item_text_fields)
    item_int_fields = json.loads(collection.item_int_fields)
    item_bool_fields = json.loads(collection.item_bool_fields)
    item_date_fields = json.loads(collection.item_date_fields)

    try:
        for field_name in item_text_fields:
            if not data[field_name]:
                return False, 'no {0} data in field for item'.format(field_name)

        for field_name in item_int_fields:
            if not data[field_name]:
                return False, 'no {0} data in field for item'.format(field_name)
            elif not isinstance(data[field_name], int):
                return False, 'Incorrect type of {0} field, must be integer'.format(field_name)

        for field_name in item_bool_fields:
            if data[field_name] != 0 and not data[field_name]:
                return False, 'no {0} data in field for item'.format(field_name)
            elif not isinstance(data[field_name], int) or (data[field_name] != 0 and data[field_name] != 1):
                return False, 'Incorrect type of {0} field, must be 1 or 0'.format(field_name)

        for field_name in item_date_fields:
            if not data[field_name]:
                return False, 'no {0} data in field for item'.format(field_name)
            datetime.datetime.strptime(data[field_name], '%Y-%m-%d')

        for key, value in data.items():
            if not (key in item_text_fields or key in item_int_fields or key in item_date_fields or key in item_bool_fields):
                return False, 'extra fields must not be included'

    except KeyError as e:
        return False, {'no field {0} for item'.format(e)}

    return True, 'ok'


def validate_tags(data):
    try:
        if not isinstance(data, list):
            return False, 'tags must be type of list'
        for item in data:
            if not isinstance(item, str) or len(item) >= 50:
                return False, 'tag must be str, tag must be less than 50 symbols'
        return True, 'ok'
    except Exception as e:
        return False, 'incorrect request, must be [{name:<tag_name>},...]'
