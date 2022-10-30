from django.urls import path

from . import views


app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('<int:user_id>/', views.student_card, name='student_card')
]
