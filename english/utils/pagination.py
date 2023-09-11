from django.core.paginator import Page, Paginator
from django.db.models.query import QuerySet


def paginator(
    page_number: int | str | None, objects: QuerySet, per_page: int
) -> Page:
    """Paginator for function based views."""
    paginator = Paginator(objects, per_page)
    return paginator.get_page(page_number)
