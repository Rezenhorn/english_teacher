from django.urls import path

from .views import AboutAuthorView, IndexView

app_name = 'about'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutAuthorView.as_view(), name='about'),
]