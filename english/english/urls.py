from django.contrib import admin
from django.urls import include, path

handler404 = "core.views.page_not_found"
handler403 = "core.views.csrf_failure"
handler500 = "core.views.internal_error"

urlpatterns = [
    path("", include("about.urls", namespace="about")),
    path("students/", include("students.urls", namespace="students")),
    path("dictionary/", include("dictionary.urls", namespace="dictionary")),
    path("quiz/", include("quiz.urls", namespace="quiz")),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls", namespace="users")),
    path("auth/", include("django.contrib.auth.urls")),
]
