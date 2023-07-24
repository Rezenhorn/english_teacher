from typing import Iterable, Literal

from django.db.models import Q
from users.models import User

from .models import Dictionary


def get_words(
    *,
    student: User,
    search_query: str | None,
    ordering: Literal["date", "word"] | None
) -> Iterable[Dictionary]:
    """
    Returns Dictionary objects of a student
    filtered with search_query with needed ordering.
    """
    queryset = Dictionary.objects.filter(student=student)
    if search_query:
        queryset = queryset.filter(
            Q(word__icontains=search_query)
            | Q(translation__icontains=search_query)
        )
    if ordering == "date":
        queryset = queryset.order_by("-date", "word")
    return queryset
