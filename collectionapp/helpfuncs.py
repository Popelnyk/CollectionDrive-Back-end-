from json import JSONDecodeError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json

from collectionapp.models import Item, Tag


def create_or_add_tags(validated_data, item):
    try:
        tags_from_json = json.loads(validated_data)
    except JSONDecodeError as e:
        return Response('incorrect tags, must be [\'<tag_name>\',...]', status=status.HTTP_400_BAD_REQUEST)

    print(tags_from_json)
    for data in tags_from_json:
        data = str.lower(data)

        if Tag.objects.filter(description__exact=data).count() == 0:
            Tag.objects.create(description=data)

        tag = Tag.objects.get(description__exact=data)
        tag.item.add(item)
        tag.save()
