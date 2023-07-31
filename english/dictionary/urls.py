from django.urls import path

from . import views

app_name = "dictionary"

urlpatterns = [
    path("<str:username>/", views.WordListView.as_view(), name="dictionary"),
    path("<str:username>/add_word/",
         views.WordCreateView.as_view(),
         name="add_word"),
    path("<str:username>/edit_word/<int:word_id>/",
         views.WordUpdateView.as_view(),
         name="edit_word"),
    path("<str:username>/delete_word/<int:word_id>/",
         views.WordDeleteView.as_view(),
         name="delete_word"),
    path("<str:username>/download",
         views.download_dictionary,
         name="download_dictionary"),
]
