from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.StudentListView.as_view(), name="list"),
    path("<str:username>/", views.student_card, name="student_card"),
    path("<str:username>/add_homework/",
         views.HomeworkCreateView.as_view(),
         name="add_homework"),
    path("<str:username>/edit_homework/<int:homework_id>/",
         views.HomeworkUpdateView.as_view(),
         name="edit_homework"),
    path("<str:username>/delete_homework/<int:homework_id>/",
         views.HomeworkDeleteView.as_view(),
         name="delete_homework"),
    path("<str:username>/dictionary/",
         views.DictionaryListView.as_view(),
         name="dictionary"),
    path("<str:username>/dictionary/add_word/",
         views.DictionaryCreateView.as_view(),
         name="add_word"),
    path("<str:username>/progress/",
         views.ProgressListView.as_view(),
         name="progress"),
    path("<str:username>/dictionary/download",
         views.download_dictionary,
         name="download_dictionary")
]
