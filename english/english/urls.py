from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("about.urls", namespace="about")),
    path("students/", include("students.urls", namespace="students")),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include("django.contrib.auth.urls")),
]
