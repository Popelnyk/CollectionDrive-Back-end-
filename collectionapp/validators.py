def validate_item_fields(data):
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, str):
                raise TypeError('names of fields can be strings only')
    else:
        raise TypeError('fields must be included in a list')
