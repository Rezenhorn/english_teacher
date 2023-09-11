from django.core import serializers
from django.core.paginator import Page, Paginator
from django.db.models.query import QuerySet


def serialize_queryset(queryset: QuerySet) -> str:
    """Serialize queryset into json."""
    return serializers.serialize("json", queryset)


def deserialize_queryset(json: str) -> list:
    """Deserialize json with queryset into objects list."""
    deserialized = serializers.deserialize("json", json)
    return list(map(lambda x: x.object, deserialized))


def serialize_page_object(page_obj: Page) -> dict:
    """Serialize `Page` object into json."""
    return {
        "object_list": serializers.serialize("json", page_obj),
        "paginator": {
            "per_page": page_obj.paginator.per_page,
        },
        "number": page_obj.number
    }


def deserialize_page_object(json: dict) -> Page:
    """Deserialize `Page` from json."""
    return Page(
        object_list=deserialize_queryset(json["object_list"]),
        number=json["number"],
        paginator=Paginator(
            object_list=json["object_list"],
            per_page=json["paginator"]["per_page"],
        )
    )
