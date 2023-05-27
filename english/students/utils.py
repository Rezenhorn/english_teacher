from functools import wraps

import xlwt
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

User = get_user_model()


def create_dictionary_xls(username: str) -> xlwt.Workbook:
    """Return the excel workbook with student's dictionary."""
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("Dictionary")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Word", "Transcription", "Translation", "Example"]

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    user = get_object_or_404(User, username=username)
    rows = user.dictionary.values_list(
        "word", "transcription", "translation", "example"
    )

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), font_style)
    return workbook


def author_or_superuser_required(func):
    """Decorator that checks if the user is an owner of the page
    or superuser.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        username = kwargs.get("username")
        if not (request.user.is_superuser
                or request.user.username == username):
            return redirect("about:index")
        return func(request, *args, **kwargs)
    return wrapper
