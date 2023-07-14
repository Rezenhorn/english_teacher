from django.urls import path

from . import views

app_name = "quiz"

urlpatterns = [
    path("<str:username>/create/",
         views.SetupQuizFormView.as_view(),
         name="quiz_setup"),
    path("<str:username>/<int:quiz_id>/", views.quiz_view, name="quiz"),
]
