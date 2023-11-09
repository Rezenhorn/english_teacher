from typing import Iterable

from .models import Word


def search_words(
    search_query: str, queryset: Iterable[Word]
) -> Iterable[Word]:
    """Search for words in given queryset."""
    result = queryset
    if len(search_query) > 2:
        result = filter(
            lambda word: search_query.lower() in word.translation.lower()
            or search_query.lower() in word.word.lower(),
            queryset
        )
    return result


def order_words(ordering: str, queryset: Iterable[Word]) -> list[Word]:
    """Sorts the queryset by the given ordering."""
    match ordering:
        case "date":
            return sorted(
                queryset, key=lambda word: word.date, reverse=True
            )
        case "translation":
            return sorted(
                queryset,
                key=lambda word: word.translation.lower()
            )
    return queryset
