from django.urls import path

from . import views

app_name = "dictionary"

urlpatterns = [
    path("<str:username>/",
         views.DictionaryListView.as_view(),
         name="dictionary"),
    path("<str:username>/add_word/",
         views.DictionaryCreateView.as_view(),
         name="add_word"),
    path("<str:username>/edit_word/<int:dictionary_id>/",
         views.DictionaryUpdateView.as_view(),
         name="edit_word"),
    path("<str:username>/download",
         views.download_dictionary,
         name="download_dictionary"),
    path("<str:username>/setup_quiz/",
         views.SetupQuizFormView.as_view(),
         name="setup_quiz"),
    path("<str:username>/quiz/<str:mode>/<int:number_of_words>",
         views.quiz_view,
         name="quiz"),
    path("<str:username>/quiz_result/<int:score>/",
         views.quiz_result_view,
         name="quiz_result"),
]
